"""LangGraph flow for routing user requests to external tools."""

from __future__ import annotations

from typing import Dict, Any
import os

import openai
from langgraph.graph import StateGraph, END

from tools.crm_tool import crm_tool
from tools.scm_tool import scm_tool
from tools.retry import retry_async


FUNCTIONS = [
    {
        "name": "crm_tool",
        "description": "Query the CRM (SalesForce) system",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Question from the user to send to the CRM API",
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "scm_tool",
        "description": "Query the SCM (o9) system",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Question from the user to send to the SCM API",
                }
            },
            "required": ["query"],
        },
    },
]


async def router(state: Dict[str, Any]) -> str:
    """Use an LLM to decide which tool to call."""
    user_input = state.get("user_input", "")

    async def _call_openai(messages):
        return await openai.ChatCompletion.acreate(
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo-0613"),
            messages=messages,
            functions=FUNCTIONS,
            function_call="auto",
        )

    messages = [{"role": "user", "content": user_input}]
    response = await retry_async(_call_openai, messages=messages)
    choice = response.choices[0]
    if choice.finish_reason == "function_call" and choice.message.function_call:
        name = choice.message.function_call.name
        if name == "crm_tool":
            return "crm"
        if name == "scm_tool":
            return "scm"
    # default route: choose CRM if no function call is produced
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
