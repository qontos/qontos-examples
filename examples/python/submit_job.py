#!/usr/bin/env python3
"""Submit a quantum job to QONTOS.

Demonstrates the full lifecycle of a quantum job submission:
  1. Connect to the QONTOS API
  2. Submit an OpenQASM 2.0 circuit
  3. Poll for completion
  4. Retrieve and inspect results

Usage:
    export QONTOS_API_KEY="your-api-key"
    python submit_job.py
"""

from qontos import QontosClient

# ---------------------------------------------------------------------------
# 1. Initialize the client
# ---------------------------------------------------------------------------
# Point at your local dev server or the hosted QONTOS endpoint.
# The API key can also be read from the QONTOS_API_KEY environment variable.
client = QontosClient(api_url="http://localhost:8000", api_key="demo")

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
job = client.submit(
    circuit=bell_qasm,
    input_type="openqasm",
    shots=4096,
    name="Bell State Demo",
    tags={"source": "qontos-examples", "level": "beginner"},
)
print(f"  Job ID : {job.job_id}")
print(f"  Status : {job.status}")

# ---------------------------------------------------------------------------
# 4. Wait for the result
# ---------------------------------------------------------------------------
print("Waiting for results...")
result = client.wait(job.job_id, timeout_seconds=120, poll_interval=2.0)

# ---------------------------------------------------------------------------
# 5. Inspect the result
# ---------------------------------------------------------------------------
print(f"\n--- Results for job {job.job_id} ---")
print(f"  Backend        : {result.backend}")
print(f"  Shots executed : {result.shots}")
print(f"  Elapsed (ms)   : {result.elapsed_ms:.1f}")
print(f"  Counts:")
for bitstring, count in sorted(result.counts.items()):
    pct = 100 * count / result.shots
    print(f"    |{bitstring}> : {count:>5}  ({pct:.1f}%)")

# For a Bell state we expect roughly equal |00> and |11>.
print("\nDone.")
