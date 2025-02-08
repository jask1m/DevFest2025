from langgraph.graph import StateGraph
from agents.criteria_agent import criteria_agent
from agents.new_criteria_agent import new_criteria_agent
from agents.qa_agent import qa_agent
from utils.models import GraphState

def create_workflow():
    builder = StateGraph(GraphState)
    builder.add_node("criteria_agent", criteria_agent)
    builder.add_node("new_criteria_agent", new_criteria_agent)
    builder.add_node("qa_agent", qa_agent)
    builder.set_entry_point("criteria_agent")
    return builder.compile()