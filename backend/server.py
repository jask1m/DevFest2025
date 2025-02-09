from typing import Dict, List
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from utils.workflow import create_workflow, create_parallel_workflow
from utils.CriteriaStorage import CriteriaStorage
from utils.models import GraphState, ParallelState
import chromadb
import uuid
from sentence_transformers import SentenceTransformer
from utils.config import create_llm
from typing import Dict, List, Any
import os
from groq import Groq

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

groq_client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

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
        res = workflow.invoke(initial_state, config={"recursion_limit": 10})  # returns a GraphState object
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
        XSS Analysis: {state["xss_agent_msg"]}
        SQLi Analysis: {state["SQLi_agent_msg"]}
        Payload Analysis: {state["payload_agent_msg"]}
        """

        embedding = embedder.encode(combined_text).tolist()
        metadata = {
            "xss_agent_msg": state["xss_agent_msg"],
            "SQLi_agent_msg": state["SQLi_agent_msg"],
            "payload_agent_msg": state["payload_agent_msg"],
            "threat_detected": state["threat_detected"],
            "feedback": state["feedback"],
        }

        collection.add(
            embeddings=[embedding],
            documents=[combined_text],
            metadatas=[metadata],
            ids=[uid],
        )
        return {
            "status": "success",
            "message": f"Stored analysis with ID: {uid}",
            "id": uid,
        }

    except Exception as e:
        print(f"Error in /store endpoint: {str(e)}")
        return {"error": str(e)}


@app.post("/generate-diagram")
async def generate_diagram(request: Request):
    try:
        data = await request.json()
        solution = data.get("solution")
        
        prompt = f"""Generate a simple, high-level Mermaid flowchart diagram for the following security solution:
                    {solution}
                    Requirements for the diagram:
                    1. Use 'flowchart TD' for vertical layout (top-down)
                    2. Keep it high-level with maximum 4-6 main nodes
                    3. Use simple, one-directional flow
                    4. Each node text should be concise (maximum 4-5 words)
                    5. Focus on the main security solution steps only
                    6. Avoid complex branching or parallel paths
                    7. Use clear, simple shapes (mainly rectangles)
                    8. DO NOT include any markdown formatting or code blocks
                    9. Start directly with 'flowchart TD'
                    Return ONLY the raw Mermaid diagram code with no additional formatting or explanation."""

        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a technical diagram generator that creates simple, high-level Mermaid flowcharts for security concepts. Return only the raw Mermaid diagram code without any markdown formatting or code blocks."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.1,
        )
        
        mermaid_code = chat_completion.choices[0].message.content.strip()
        
        # More robust cleaning of the response
        # Remove any markdown code block indicators
        mermaid_code = mermaid_code.replace("```mermaid", "")
        mermaid_code = mermaid_code.replace("```", "")
        
        # Remove any leading/trailing whitespace and newlines
        mermaid_code = mermaid_code.strip()
        
        # Ensure it starts with flowchart TD and only once
        if "flowchart TD" in mermaid_code:
            # Remove any duplicate flowchart TD declarations
            mermaid_code = mermaid_code.replace("flowchart TD", "", mermaid_code.count("flowchart TD") - 1)
        else:
            mermaid_code = "flowchart TD\n" + mermaid_code.replace("flowchart LR", "").replace("graph LR", "")
        
        # Validate basic Mermaid syntax
        if not any(["-->" in mermaid_code or "-.->" in mermaid_code or "==>" in mermaid_code]):
            raise ValueError("Invalid Mermaid diagram: No valid connections found")
            
        return {"diagram": mermaid_code}
        
    except Exception as e:
        print(f"Error in generate-diagram endpoint: {str(e)}")
        return {"error": str(e)}


@app.post("/search")
async def handle_search(request: Request):
    try:
        data = await request.json()
        query = data.get("query")
        query_embedding = embedder.encode(query).tolist()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3,
            include=["documents", "metadatas"],
        )

        if not results["documents"][0]:
            return {"response": "No relevant security analyses found."}

        rag_response = await getRAG(query, results)

        return {"response": rag_response, "matches_found": len(results["documents"][0])}

    except Exception as e:
        print(f"Error in /search endpoint: {str(e)}")
        return {"error": str(e)}


async def getRAG(query: str, search_results: Dict[str, List]) -> str:
    try:
        # Build context with clearer structure and sections
        context = ""
        for i in range(len(search_results['documents'][0])):
            metadata = search_results['metadatas'][0][i]
            context += f"\nAnalysis Record {i+1}:\n"
            context += "------\n"
            context += f"XSS Finding: {metadata['xss_agent_msg']}\n"
            context += f"SQL Injection Finding: {metadata['SQLi_agent_msg']}\n"
            context += f"Payload Finding: {metadata['payload_agent_msg']}\n"
            context += f"Threat Status: {'⚠️ Threat Detected' if metadata['threat_detected'] else 'No Threat Detected'}\n"
            context += f"Security Note: {metadata['feedback']}\n"
            context += "------\n"

        prompt = f"""You are a specialized rag search engine. Your task is to answer the following query using only the provided security analysis records.

        User Query: "{query}"

        Security Analysis Records:
        {context}

        Using this information, generate a response that is concise, specific, and supports findings with direct quotes. Additionally, based on the response and information about malicious activity, include three actionable steps the user can take to handle this based on what the security analysis records say."""

        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a security search engine assistant that provides evidence-based answers using only information from security analysis records. Always support findings with direct quotes."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.1,
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        print(f"Error in getRAG: {str(e)}")
        raise e