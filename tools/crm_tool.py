"""Placeholder CRM tool used by the autonomous agent."""

import asyncio
from .retry import retry_async

async def _call_crm_api(query: str) -> str:
    """Placeholder for CRM API call."""
    await asyncio.sleep(0.1)  # simulate network latency
    return f"CRM response to: {query}"

async def crm_tool(query: str) -> str:
    """Call the CRM API with retry."""
    return await retry_async(_call_crm_api, query=query)
