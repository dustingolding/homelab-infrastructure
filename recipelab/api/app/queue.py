import json
import os
from dataclasses import dataclass
from typing import Any

import redis


@dataclass
class Job:
    job_type: str
    payload: dict[str, Any]

    def to_json(self) -> str:
        return json.dumps({"job_type": self.job_type, "payload": self.payload})


class Queue:
    def __init__(self) -> None:
        host = os.getenv("REDIS_HOST", "recipelab-redis")
        port = int(os.getenv("REDIS_PORT", "6379"))
        password = os.getenv("REDIS_PASSWORD")
        self._queue_name = os.getenv("RECIPES_JOB_QUEUE", "recipelab:jobs")
        self._client = redis.Redis(host=host, port=port, password=password, decode_responses=True)

    def enqueue(self, job: Job) -> None:
        self._client.lpush(self._queue_name, job.to_json())
