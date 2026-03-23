#!/usr/bin/env python3
"""Execute circuits on Amazon Braket via QONTOS (requires AWS credentials).

This example demonstrates how to configure and use an Amazon Braket backend
through the QONTOS orchestration layer. The QONTOS SDK provides a unified
interface -- the same code structure works for any backend.

NOTE: Running this example requires:
  - An AWS account with Amazon Braket access
  - Valid AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
  - The QONTOS instance must have the Braket provider configured

Without real credentials, this script will fail at job submission.
The local simulator example (local_simulator.py) works without credentials.

Usage:
    export QONTOS_API_KEY="your-api-key"
    export QONTOS_BASE_URL="http://localhost:8000"
    export AWS_ACCESS_KEY_ID="your-aws-key"
    export AWS_SECRET_ACCESS_KEY="your-aws-secret"
    export AWS_DEFAULT_REGION="us-east-1"
    python amazon_braket.py
"""

import os

from qontos import QontosClient

# ---------------------------------------------------------------------------
# 1. Initialize the QONTOS client
# ---------------------------------------------------------------------------
client = QontosClient(
    base_url=os.getenv("QONTOS_BASE_URL", "http://localhost:8000"),
    api_key=os.getenv("QONTOS_API_KEY", "demo"),
)

# ---------------------------------------------------------------------------
# 2. Configure Amazon Braket backend preferences
# ---------------------------------------------------------------------------
# QONTOS routes jobs to Amazon Braket when you specify the provider.
# The platform handles circuit translation to Braket's format, queue
# management, and result retrieval.
braket_config = {
    "provider": "amazon_braket",
    "aws_region": os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    # Optional: specify a particular device
    # "device_arn": "arn:aws:braket:us-east-1::device/qpu/ionq/Harmony",
    # For testing, you can target the Braket local simulator:
    # "device_arn": "arn:aws:braket:::device/quantum-simulator/amazon/sv1",
}

if not os.getenv("AWS_ACCESS_KEY_ID"):
    print("WARNING: AWS_ACCESS_KEY_ID not set. Job submission will fail.")
    print("Set AWS credentials or use local_simulator.py instead.")

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
# 4. Submit the job targeting Amazon Braket
# ---------------------------------------------------------------------------
print("Submitting Bell-state circuit to Amazon Braket...")
job = client.submit_job(
    circuit=bell_qasm,
    shots=4096,
    name="Amazon Braket Demo",
    backend_config=braket_config,
    tags={"source": "qontos-examples", "provider": "amazon_braket"},
)
print(f"  Job ID : {job.id}")
print(f"  Status : {job.status}")

# ---------------------------------------------------------------------------
# 5. Wait for results
# ---------------------------------------------------------------------------
print("Waiting for results...")
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
