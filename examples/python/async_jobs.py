#!/usr/bin/env python3
"""Asynchronous job submission and polling with QONTOS.

Demonstrates how to use the AsyncQontosClient to submit multiple quantum
jobs concurrently and poll for their completion. This is the recommended
approach for batch workloads where you want to maximize throughput.

Usage:
    export QONTOS_API_KEY="your-api-key"
    export QONTOS_BASE_URL="http://localhost:8000"
    python async_jobs.py
"""

from __future__ import annotations

import asyncio
import os
import time

from qontos import AsyncQontosClient

# ---------------------------------------------------------------------------
# 1. Define circuits to submit
# ---------------------------------------------------------------------------
# We submit three circuits of increasing size concurrently.

CIRCUITS = {
    "Hadamard (1Q)": """\
OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
creg c[1];
h q[0];
measure q[0] -> c[0];
""",
    "Bell State (2Q)": """\
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q[0] -> c[0];
measure q[1] -> c[1];
""",
    "GHZ-3 (3Q)": """\
OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg c[3];
h q[0];
cx q[0],q[1];
cx q[1],q[2];
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
""",
}


async def main() -> None:
    # -------------------------------------------------------------------
    # 2. Initialize the async client
    # -------------------------------------------------------------------
    async with AsyncQontosClient(
        api_key=os.getenv("QONTOS_API_KEY", "demo"),
        base_url=os.getenv("QONTOS_BASE_URL", "http://localhost:8000"),
    ) as client:

        # ---------------------------------------------------------------
        # 3. Submit all circuits concurrently
        # ---------------------------------------------------------------
        print("Submitting jobs concurrently...")
        start = time.monotonic()

        submit_tasks = []
        for name, qasm in CIRCUITS.items():
            task = client.submit_job(
                circuit=qasm,
                shots=4096,
                name=name,
                tags={"source": "qontos-examples", "example": "async_jobs"},
            )
            submit_tasks.append((name, task))

        # Gather all submissions
        jobs = {}
        for name, task in submit_tasks:
            job = await task
            jobs[name] = job
            print(f"  Submitted: {name} -> Job ID {job.id}")

        elapsed_submit = time.monotonic() - start
        print(f"\nAll {len(jobs)} jobs submitted in {elapsed_submit:.2f}s")

        # ---------------------------------------------------------------
        # 4. Poll all jobs until complete
        # ---------------------------------------------------------------
        print("\nPolling for completion...")

        completed_jobs = {}
        for name, job in jobs.items():
            completed = await client.wait_for_job(job.id, timeout=120)
            completed_jobs[name] = completed
            print(f"  {name}: status={completed.status}, outcome={completed.outcome}")

        elapsed_total = time.monotonic() - start
        print(f"\nAll jobs completed in {elapsed_total:.2f}s")

        # ---------------------------------------------------------------
        # 5. Collect and display results
        # ---------------------------------------------------------------
        print("\n" + "=" * 60)
        print("Results Summary")
        print("=" * 60)

        for name, job in completed_jobs.items():
            print(f"\n--- {name} ---")
            print(f"  Job ID  : {job.id}")
            print(f"  Status  : {job.status}")
            print(f"  Outcome : {job.outcome}")

            if job.runs:
                result = await client.get_results(job.runs[0].id)
                print(f"  Shots   : {result.total_shots}")
                print(f"  Latency : {result.latency_ms:.1f} ms")
                print("  Counts  :")
                for bitstring, count in sorted(result.counts.items()):
                    pct = 100 * count / max(1, result.total_shots)
                    print(f"    |{bitstring}> : {count:>5}  ({pct:.1f}%)")
            else:
                print("  No runs returned.")

    print("\nDone.")


if __name__ == "__main__":
    asyncio.run(main())
