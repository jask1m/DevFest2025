from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from utils.workflow import create_workflow, create_parallel_workflow
from utils.CriteriaStorage import CriteriaStorage
from utils.models import GraphState, ParallelState
import chromadb
import uuid
from sentence_transformers import SentenceTransformer
from utils.config import create_llm


app = FastAPI()
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
workflow = create_workflow()
criteria_storage = CriteriaStorage()
parallel_workflow = create_parallel_workflow()

chroma_client = chromadb.PersistentClient(path="./chroma")
collection = chroma_client.get_or_create_collection(name="collection")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/query")
async def handle_query(request: Request):
    data = await request.json()
    user_input = data.get("query")
    print("user input: ", user_input)

    current_criteria = criteria_storage.get_criteria()
    print("num critera before llm call", len(current_criteria))

    initial_state = GraphState(
        description=user_input,
        existing_criteria=current_criteria,
        selected_criteria=None,
        sent_from=None,
        feedback=None,
        approved=False,
    )

    try:
        res = workflow.invoke(initial_state)  # returns a GraphState object
        new_criteria_list = res["existing_criteria"]

        if new_criteria_list != current_criteria:
            criteria_storage.update_criteria(new_criteria_list)
            print("num criterias after llm call: ", len(new_criteria_list))

        print("FINAL LOG: ", res["selected_criteria"])
        return {"response": res}

    except Exception as e:
        return {"error": str(e)}


@app.post("/analysis")
async def handle_analysis(request: Request):
    print("reached the /analysis endpoint")
    data = await request.json()
    packet = data.get("packet")

    start_state = ParallelState(
        packet=packet,
        xss_agent_msg="",
        SQLi_agent_msg="",
        payload_agent_msg="",
        threat_detected=False,
        feedback="",
    )

    try:
        res = parallel_workflow.invoke(start_state)
        print("FINAL OUTPUT: ", res)
        return {"response": res}
    except Exception as e:
        print("ERROR invoking the chain in /analysis:", e)
        return {"error": str(e)}


@app.post("/store")
async def handle_store(request: Request):
    try:
        data = await request.json()
        state: ParallelState = data.get("state")
        
        if not state:
            return {"error": "No state provided"}


        uid = str(uuid.uuid4())
        combined_text = f"""
        XSS Analysis: {state['xss_agent_msg']}
        SQLi Analysis: {state['SQLi_agent_msg']}
        Payload Analysis: {state['payload_agent_msg']}
        """
        

        embedding = embedder.encode(combined_text).tolist()
        metadata = {
            "xss_agent_msg": state['xss_agent_msg'],
            "SQLi_agent_msg": state['SQLi_agent_msg'],
            "payload_agent_msg": state['payload_agent_msg'],
            "threat_detected": state['threat_detected'],
            "feedback": state['feedback']
        }

        collection.add(
            embeddings=[embedding],
            documents=[combined_text],
            metadatas=[metadata],
            ids=[uid]
        )
        return {
            "status": "success",
            "message": f"Stored analysis with ID: {uid}",
            "id": uid
        }
        
    except Exception as e:
        print(f"Error in /store endpoint: {str(e)}")
        return {"error": str(e)}


@app.get("/search")
async def handle_search(query: str):
    try:
        query_embedding = embedder.encode(query).tolist()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3,
            include=["documents", "metadatas"]
        )
        
        if not results['documents'][0]:
            return {"response": "No relevant security analyses found."}
        
        rag_response = await getRAG(query, results)
        
        return {
            "response": rag_response,
            "matches_found": len(results['documents'][0])
        }
        
    except Exception as e:
        print(f"Error in /search endpoint: {str(e)}")
        return {"error": str(e)}


async def getRAG(query: str, search_results: Dict[str, List]) -> str:
    try:
        context = ""
        for i in range(len(search_results['documents'][0])):
            metadata = search_results['metadatas'][0][i]
            context += f"\nSecurity Analysis {i+1}:\n"
            context += f"XSS Analysis: {metadata['xss_agent_msg']}\n"
            context += f"SQL Injection Analysis: {metadata['SQLi_agent_msg']}\n"
            context += f"Payload Analysis: {metadata['payload_agent_msg']}\n"
            context += f"Threat Detected: {metadata['threat_detected']}\n"
            context += f"Feedback: {metadata['feedback']}\n"
            context += "-" * 50 + "\n"

        prompt = f"""Given the following security analyses and the user's question: "{query}", 
        provide a comprehensive yet concise summary of the relevant findings.
        
        Security Analyses:
        {context}
        
        Please analyze these results and provide:
        1. A direct answer to the user's question
        2. Key findings from the relevant security analyses
        3. Any patterns or notable concerns that should be highlighted
        
        Keep the response focused and relevant to the user's specific query."""

        llm = create_llm()

        messages = [
            {
                "role": "system",
                "content": "You are a cybersecurity analysis assistant. Provide clear, accurate summaries of security findings.",
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        response = llm.chat.completions.create(
            messages=messages,
            temperature=0.1,
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error in getRAG: {str(e)}")
        raise e