from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated

#reducer function
def combine_responses(existing, new):
    #existing is list of ops, from prev nodes
    if not existing:
        return new
    return existing + " | " + new

class AgentState(TypedDict):
    responses: Annotated[str, combine_responses]

# Agent nodes
def agent1(state: AgentState):
    return {"responses": "Hello from agent1."}


def agent2(state: AgentState):
    return {"responses": "ELOO FROM AGENT2!!!!"}

# Create graph
graph = StateGraph(AgentState)

graph.add_node("agent1", agent1)
graph.add_node("agent2", agent2)

# Execute both agents in parallel
graph.add_edge(START, "agent1")
graph.add_edge(START, "agent2")

graph.add_edge("agent1", END)
graph.add_edge("agent2", END)

# Compile and execute
app = graph.compile()

result = app.invoke({"responses": ""})

print(result["responses"])
