#!/usr/bin/env python3
"""Execute circuits on native QONTOS modular quantum hardware.

NOTE: Native QONTOS hardware is currently in development. This example
demonstrates the future execution path using the same SDK interface.
When native hardware becomes available, no code changes will be required.

The key insight: QONTOS is a full-stack quantum computing company. The same
QontosClient API that works today with third-party backends (IBM, Amazon)
will work identically with native QONTOS modular hardware. This is the
power of the orchestration layer -- backend independence.

Usage (future, when native hardware is available):
    export QONTOS_API_KEY="your-api-key"
    export QONTOS_BASE_URL="https://api.qontos.io"
    python native_qontos.py
"""

import os

from qontos import QontosClient

# ---------------------------------------------------------------------------
# 1. Initialize the QONTOS client
# ---------------------------------------------------------------------------
# Same client initialization as every other example. The only difference
# is the backend_config at submission time.
client = QontosClient(
    base_url=os.getenv("QONTOS_BASE_URL", "http://localhost:8000"),
    api_key=os.getenv("QONTOS_API_KEY", "demo"),
)

# ---------------------------------------------------------------------------
# 2. Configure native QONTOS backend
# ---------------------------------------------------------------------------
# When native hardware is available, target it by specifying the provider.
# The QONTOS platform will:
#   - Normalize the circuit
#   - Partition it across physical quantum modules
#   - Schedule partitions on native modular hardware
#   - Stitch results together with full execution proofs
#
# No changes to your code are needed -- same API, different backend.
native_config = {
    "provider": "qontos_native",
    # Future options may include:
    # "module_topology": "linear",       # Physical module arrangement
    # "interconnect": "photonic",        # Inter-module link type
    # "error_mitigation": True,          # Enable built-in error mitigation
}

# ---------------------------------------------------------------------------
# 3. Define a circuit
# ---------------------------------------------------------------------------
# The same circuit format works for all backends.
ghz3_qasm = """\
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
"""

# ---------------------------------------------------------------------------
# 4. Submit the job targeting native QONTOS hardware
# ---------------------------------------------------------------------------
print("QONTOS Native Hardware Example")
print("=" * 60)
print()
print("NOTE: Native hardware is in development. This example shows the")
print("future execution path. The SDK interface will not change.")
print()

print("Submitting GHZ-3 circuit to native QONTOS backend...")
job = client.submit_job(
    circuit=ghz3_qasm,
    shots=4096,
    name="Native QONTOS Demo",
    backend_config=native_config,
    tags={"source": "qontos-examples", "provider": "qontos_native"},
)
print(f"  Job ID : {job.id}")
print(f"  Status : {job.status}")

# ---------------------------------------------------------------------------
# 5. Wait for results
# ---------------------------------------------------------------------------
# On native hardware, QONTOS will automatically:
#   1. Partition the circuit if it spans multiple modules
#   2. Route partitions to the optimal physical modules
#   3. Manage inter-module entanglement via photonic links
#   4. Aggregate results and generate cryptographic proofs
print("\nWaiting for results...")
job = client.wait_for_job(job.id, timeout=120, poll_interval=2.0)

print(f"\n--- Results ---")
print(f"  Status  : {job.status}")
print(f"  Outcome : {job.outcome}")

if job.runs:
    run = job.runs[0]
    result = client.get_results(run.id)
    print(f"  Shots   : {result.total_shots}")
    print(f"  Latency : {result.latency_ms:.1f} ms")
    print("  Counts  :")
    for bitstring, count in sorted(result.counts.items()):
        pct = 100 * count / max(1, result.total_shots)
        print(f"    |{bitstring}> : {count:>5}  ({pct:.1f}%)")

    # For a GHZ state, we expect |000> and |111> each near 50%
    total_ghz = result.counts.get("000", 0) + result.counts.get("111", 0)
    ghz_fidelity = total_ghz / max(1, result.total_shots)
    print(f"\n  GHZ fidelity estimate: {ghz_fidelity:.4f}")
else:
    print("  No runs returned.")

# ---------------------------------------------------------------------------
# 6. The full-stack story
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("The QONTOS Full-Stack Advantage")
print("=" * 60)
print("""
  Today:   QontosClient -> IBM / Amazon / Local Simulator
  Future:  QontosClient -> Native QONTOS Modular Hardware

  Same API. Same SDK. Same pipeline.
  Your code stays the same -- only the backend changes.
""")

# ---------------------------------------------------------------------------
# 7. Clean up
# ---------------------------------------------------------------------------
client.close()
print("Done.")
