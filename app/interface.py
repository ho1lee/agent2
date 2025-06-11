"""Gradio interface for interacting with the agent."""

import asyncio
import gradio as gr

from .agent_flow import run_agent


async def respond(message: str) -> str:
    return await run_agent(message)


def create_interface() -> gr.Interface:
    async def _fn(message: str) -> str:
        return await respond(message)

    demo = gr.Interface(fn=lambda message: asyncio.run(_fn(message)),
                        inputs=gr.Textbox(lines=1, placeholder="Ask a question"),
                        outputs="text",
                        title="Autonomous Agent")
    return demo
