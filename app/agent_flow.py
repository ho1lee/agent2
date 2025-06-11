"""LangGraph flow for routing user requests to external tools."""

from __future__ import annotations

from typing import Dict, Any
from langgraph.graph import StateGraph, END

from tools.crm_tool import crm_tool
from tools.scm_tool import scm_tool


async def router(state: Dict[str, Any]) -> str:
    """Decide which tool to call based on user input."""
    user_input = state.get("user_input", "").lower()
    if "crm" in user_input:
        return "crm"
    if "scm" in user_input:
        return "scm"
    # default route: choose CRM
    return "crm"


action_map = {
    "crm": crm_tool,
    "scm": scm_tool,
}


async def tool_node(state: Dict[str, Any], tool_name: str) -> Dict[str, Any]:
    """Execute the selected tool and update state."""
    query = state.get("user_input", "")
    tool = action_map[tool_name]
    result = await tool(query)
    return {"result": result}


def build_graph() -> StateGraph:
    graph = StateGraph()
    graph.add_node("router", router)
    graph.add_conditional_edges("router", {"crm": "crm_node", "scm": "scm_node"})
    graph.add_node("crm_node", lambda state: tool_node(state, "crm"))
    graph.add_node("scm_node", lambda state: tool_node(state, "scm"))
    graph.add_edge("crm_node", END)
    graph.add_edge("scm_node", END)
    graph.set_entry_point("router")
    return graph


async def run_agent(user_input: str) -> str:
    graph = build_graph().compile()
    state = {"user_input": user_input}
    result_state = await graph.arun(state)
    return result_state.get("result", "")
