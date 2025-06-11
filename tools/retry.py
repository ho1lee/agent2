"""Utility providing async retry logic with exponential backoff."""

import asyncio
from typing import Callable, Any, Awaitable

async def retry_async(
    func: Callable[..., Awaitable[Any]],
    *args: Any,
    max_attempts: int = 3,
    delay: float = 1.0,
    factor: float = 2.0,
    **kwargs: Any,
) -> Any:
    """Retry an async function with exponential backoff."""
    attempt = 0
    current_delay = delay
    while True:
        try:
            return await func(*args, **kwargs)
        except Exception as exc:
            attempt += 1
            if attempt >= max_attempts:
                raise
            await asyncio.sleep(current_delay)
            current_delay *= factor
