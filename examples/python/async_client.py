#!/usr/bin/env python3
"""List recent jobs with the asynchronous QONTOS client.

This example is intentionally lightweight: it exercises the async SDK surface
without requiring custom orchestration logic in the examples repo.

Usage:
    export QONTOS_API_KEY="your-api-key"
    export QONTOS_BASE_URL="http://localhost:8000"
    python async_client.py
"""

from __future__ import annotations

import asyncio
import os

from qontos import AsyncQontosClient


async def main() -> None:
    async with AsyncQontosClient(
        api_key=os.getenv("QONTOS_API_KEY", "demo"),
        base_url=os.getenv("QONTOS_BASE_URL", "http://localhost:8000"),
    ) as client:
        jobs = await client.list_jobs(limit=5)
        print("Recent jobs:")
        if not jobs:
            print("  No jobs returned by the API.")
            return
        for job in jobs:
            print(f"  {job.id}  status={job.status}  outcome={job.outcome}")


if __name__ == "__main__":
    asyncio.run(main())
