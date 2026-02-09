import json
import os
from typing import Any

import redis


class Queue:
    def __init__(self) -> None:
        host = os.getenv("REDIS_HOST", "recipelab-redis")
        port = int(os.getenv("REDIS_PORT", "6379"))
        password = os.getenv("REDIS_PASSWORD")
        self._queue_name = os.getenv("RECIPES_JOB_QUEUE", "recipelab:jobs")
        self._client = redis.Redis(host=host, port=port, password=password, decode_responses=True)

    def pop(self, timeout: int = 5) -> dict[str, Any] | None:
        result = self._client.brpop(self._queue_name, timeout=timeout)
        if not result:
            return None
        _, payload = result
        return json.loads(payload)
