from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from utils.workflow import create_workflow, create_parallel_workflow
from utils.CriteriaStorage import CriteriaStorage
from utils.models import GraphState, ParallelState
import json

app = FastAPI()
origins = ["*"]
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
      approved=False
    )

  try:
    res = workflow.invoke(initial_state) # returns a GraphState object
    new_criteria_list = res['existing_criteria']

    if new_criteria_list != current_criteria:
      criteria_storage.update_criteria(new_criteria_list)
      print("num criterias after llm call: ", len(new_criteria_list))

    print("FINAL LOG: ", res['selected_criteria'])
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