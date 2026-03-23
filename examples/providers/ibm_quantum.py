#!/usr/bin/env python3
# Status: requires credentials (IBM Quantum account)
"""Execute circuits on IBM Quantum via QONTOS (requires IBM credentials).

This example demonstrates how to configure and use an IBM Quantum backend
through the QONTOS orchestration layer. The QONTOS SDK provides a unified
interface -- the same code structure works for any backend.

NOTE: Running this example requires:
  - An IBM Quantum account (https://quantum.ibm.com)
  - A valid IBM API token set via IBMQ_API_TOKEN environment variable
  - The QONTOS instance must have the IBM provider configured

Without real credentials, this script will fail at job submission.
The local simulator example (local_simulator.py) works without credentials.

Usage:
    export QONTOS_API_KEY="your-api-key"
    export QONTOS_BASE_URL="http://localhost:8000"
    export IBMQ_API_TOKEN="your-ibm-token"
    python ibm_quantum.py
"""

import os

from qontos import QontosClient

# ---------------------------------------------------------------------------
# 1. Initialize the QONTOS client
# ---------------------------------------------------------------------------
# The QONTOS client is the same regardless of which backend you target.
# Backend selection happens at job submission time.
client = QontosClient(
    base_url=os.getenv("QONTOS_BASE_URL", "http://localhost:8000"),
    api_key=os.getenv("QONTOS_API_KEY", "demo"),
)

# ---------------------------------------------------------------------------
# 2. Configure IBM backend constraints
# ---------------------------------------------------------------------------
# QONTOS routes jobs to IBM Quantum when you specify the provider.
# The platform handles transpilation, queue management, and result retrieval.
ibm_constraints = {
    "provider": "ibm_quantum",
    "ibm_api_token": os.getenv("IBMQ_API_TOKEN"),
    # Optional: specify a particular backend
    # "backend_name": "ibm_brisbane",
}

if not ibm_constraints["ibm_api_token"]:
    print("WARNING: IBMQ_API_TOKEN not set. Job submission will fail.")
    print("Set the environment variable or use local_simulator.py instead.")

# ---------------------------------------------------------------------------
# 3. Define a Bell-state circuit
# ---------------------------------------------------------------------------
bell_qasm = """\
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q[0] -> c[0];
measure q[1] -> c[1];
"""

# ---------------------------------------------------------------------------
# 4. Submit the job targeting IBM Quantum
# ---------------------------------------------------------------------------
print("Submitting Bell-state circuit to IBM Quantum...")
job = client.submit_job(
    circuit=bell_qasm,
    shots=4096,
    name="IBM Quantum Demo",
    constraints=ibm_constraints,
    tags={"source": "qontos-examples", "provider": "ibm_quantum"},
)
print(f"  Job ID : {job.id}")
print(f"  Status : {job.status}")

# ---------------------------------------------------------------------------
# 5. Wait for results (IBM jobs may take minutes due to queue times)
# ---------------------------------------------------------------------------
print("Waiting for results (this may take several minutes on real hardware)...")
job = client.wait_for_job(job.id, timeout=600, poll_interval=10.0)

print(f"\n--- Results ---")
print(f"  Status  : {job.status}")
print(f"  Outcome : {job.outcome}")

if job.runs:
    run = job.runs[0]
    result = client.get_results(run.id)
    print(f"  Backend : {result.backend_name if hasattr(result, 'backend_name') else 'N/A'}")
    print(f"  Shots   : {result.total_shots}")
    print(f"  Latency : {result.latency_ms:.1f} ms")
    print("  Counts  :")
    for bitstring, count in sorted(result.counts.items()):
        pct = 100 * count / max(1, result.total_shots)
        print(f"    |{bitstring}> : {count:>5}  ({pct:.1f}%)")
else:
    print("  No runs returned.")

# ---------------------------------------------------------------------------
# 6. Clean up
# ---------------------------------------------------------------------------
client.close()
print("\nDone.")
