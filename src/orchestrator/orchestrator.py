from langgraph.graph import StateGraph, START
from src.agentic_core.agents import response_generator_agent
from src.memory.cache_memory import cache_memory
from langgraph.graph import MessagesState


# Build graph
builder = StateGraph(MessagesState)
builder.add_node("response_generator", response_generator_agent.response_generator_agent)
builder.add_edge(START, "response_generator")
historia = builder.compile(checkpointer=cache_memory)
