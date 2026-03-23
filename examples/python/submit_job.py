#!/usr/bin/env python3
"""Submit a quantum job to QONTOS.

Demonstrates the full lifecycle of a quantum job submission:
  1. Connect to the QONTOS API
  2. Submit an OpenQASM 2.0 circuit
  3. Poll for completion
  4. Retrieve and inspect results

Usage:
    export QONTOS_API_KEY="your-api-key"
    export QONTOS_BASE_URL="http://localhost:8000"
    python submit_job.py
"""

import os

from qontos import QontosClient

# ---------------------------------------------------------------------------
# 1. Initialize the client
# ---------------------------------------------------------------------------
# Point at your local dev server or the hosted QONTOS endpoint.
# The API key can also be read from the QONTOS_API_KEY environment variable.
client = QontosClient(
    base_url=os.getenv("QONTOS_BASE_URL", "http://localhost:8000"),
    api_key=os.getenv("QONTOS_API_KEY", "demo"),
)

# ---------------------------------------------------------------------------
# 2. Define a simple Bell-state circuit in OpenQASM 2.0
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
# 3. Submit the circuit
# ---------------------------------------------------------------------------
print("Submitting Bell-state circuit...")
job = client.submit_job(
    circuit=bell_qasm,
    shots=4096,
    name="Bell State Demo",
    tags={"source": "qontos-examples", "level": "beginner"},
)
print(f"  Job ID : {job.id}")
print(f"  Status : {job.status}")

# ---------------------------------------------------------------------------
# 4. Wait for the result
# ---------------------------------------------------------------------------
print("Waiting for results...")
job = client.wait_for_job(job.id, timeout=120, poll_interval=2.0)

# ---------------------------------------------------------------------------
# 5. Inspect the result if a run was created
# ---------------------------------------------------------------------------
print(f"\n--- Final Job Status for {job.id} ---")
print(f"  Status         : {job.status}")
print(f"  Outcome        : {job.outcome}")

if job.runs:
    run = job.runs[0]
    result = client.get_results(run.id)
    print(f"  Run ID         : {run.id}")
    print(f"  Total shots    : {result.total_shots}")
    print(f"  Latency (ms)   : {result.latency_ms}")
    print("  Counts:")
    for bitstring, count in sorted(result.counts.items()):
        pct = 100 * count / max(1, result.total_shots)
        print(f"    |{bitstring}> : {count:>5}  ({pct:.1f}%)")
else:
    print("  No runs were returned for this job yet.")

client.close()
print("\nDone.")
