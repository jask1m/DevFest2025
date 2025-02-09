from langgraph.graph import StateGraph, START, END
from agents.criteria_agent import criteria_agent
from agents.new_criteria_agent import new_criteria_agent
from agents.qa_agent import qa_agent
from agents.analysis.xss_agent import xss_agent
from agents.analysis.SQLi_agent import SQLi_agent
from agents.analysis.root_node import root_node
from agents.analysis.decision_node import decision_node
from utils.models import GraphState, ParallelState

def create_workflow():
  builder = StateGraph(GraphState)
  builder.add_node("criteria_agent", criteria_agent)
  builder.add_node("new_criteria_agent", new_criteria_agent)
  builder.add_node("qa_agent", qa_agent)
  builder.set_entry_point("criteria_agent")
  return builder.compile()

def create_parallel_workflow():
  builder = StateGraph(ParallelState)
  builder.add_node(root_node)
  builder.add_node(xss_agent)
  builder.add_node(SQLi_agent)
  builder.add_node(decision_node)
  # the rest goes here

  builder.add_edge(START, "root_node")
  builder.add_edge("root_node", "xss_agent")
  builder.add_edge("root_node", "SQLi_agent")
  # the rest goes here

  builder.add_edge("xss_agent", "decision_node")
  builder.add_edge("SQLi_agent", "decision_node")
  # the rest goes here
  builder.add_edge("decision_node", END)
  return builder.compile()