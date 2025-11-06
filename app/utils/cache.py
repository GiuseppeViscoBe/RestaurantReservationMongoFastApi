import json
from typing import Callable, Any

async def get_or_set_cache(redis, key: str, ttl: int, fetch_func: Callable[[], Any]):
    """Get cached value from Redis or call fetch_func() and store the result."""
    cached = await redis.get(key)
    if cached:
        return json.loads(cached)

    # Cache miss → fetch and store
    data = await fetch_func()
    await redis.setex(key, ttl, json.dumps(data))
    return data
