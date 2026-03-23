#!/usr/bin/env python3
# Status: requires running QONTOS API server
"""Deep inspection of QONTOS run results.

Demonstrates how to submit a quantum job and perform detailed inspection
of the RunResult object, including:
  - Measurement counts and distributions
  - Fidelity estimate
  - Aggregation method
  - Execution timing

Usage:
    export QONTOS_API_KEY="your-api-key"
    export QONTOS_BASE_URL="http://localhost:8000"
    python result_inspection.py
"""

import os

from qontos import QontosClient

# ---------------------------------------------------------------------------
# 1. Initialize the client
# ---------------------------------------------------------------------------
client = QontosClient(
    base_url=os.getenv("QONTOS_BASE_URL", "http://localhost:8000"),
    api_key=os.getenv("QONTOS_API_KEY", "demo"),
)

# ---------------------------------------------------------------------------
# 2. Define a Bell-state circuit
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
# 3. Submit and wait for results
# ---------------------------------------------------------------------------
print("Submitting Bell-state circuit...")
job = client.submit_job(
    circuit=bell_qasm,
    shots=8192,
    name="Result Inspection Demo",
    tags={"source": "qontos-examples", "example": "result_inspection"},
)
print(f"  Job ID: {job.id}")

job = client.wait_for_job(job.id, timeout=120, poll_interval=2.0)

# ---------------------------------------------------------------------------
# 4. Inspect the RunResult in detail
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("QONTOS Result Inspection")
print("=" * 60)

print(f"\nJob Status  : {job.status}")
print(f"Job Outcome : {job.outcome}")
print(f"Num Runs    : {len(job.runs) if job.runs else 0}")

if job.runs:
    run = job.runs[0]
    result = client.get_results(run.id)

    # -- Counts and distribution --
    print(f"\n--- Measurement Counts ---")
    print(f"  Total shots : {result.total_shots}")
    print(f"  Unique outcomes: {len(result.counts)}")
    print()
    for bitstring, count in sorted(result.counts.items()):
        pct = 100 * count / max(1, result.total_shots)
        bar = "#" * int(40 * count / result.total_shots)
        print(f"  |{bitstring}> : {count:>6}  ({pct:5.1f}%)  {bar}")

    # -- Fidelity estimate --
    # For a perfect Bell state, we expect only |00> and |11>.
    # The fidelity estimate measures how close we are to the ideal.
    print(f"\n--- Fidelity Analysis ---")
    ideal_outcomes = {"00", "11"}
    ideal_count = sum(
        result.counts.get(bs, 0) for bs in ideal_outcomes
    )
    estimated_fidelity = ideal_count / max(1, result.total_shots)
    print(f"  Expected outcomes : {ideal_outcomes}")
    print(f"  Ideal count       : {ideal_count}")
    print(f"  Estimated fidelity: {estimated_fidelity:.4f}")

    if hasattr(result, "fidelity_estimate") and result.fidelity_estimate is not None:
        print(f"  Platform fidelity : {result.fidelity_estimate:.4f}")

    # -- Aggregation method --
    print(f"\n--- Aggregation ---")
    if hasattr(result, "aggregation_method") and result.aggregation_method:
        print(f"  Method : {result.aggregation_method}")
    else:
        print("  Method : single-partition (no aggregation needed)")

    # -- Timing --
    print(f"\n--- Timing ---")
    print(f"  Latency (ms) : {result.latency_ms}")
    if hasattr(result, "queue_time_ms") and result.queue_time_ms is not None:
        print(f"  Queue (ms)   : {result.queue_time_ms}")
    if hasattr(result, "execution_time_ms") and result.execution_time_ms is not None:
        print(f"  Execution (ms): {result.execution_time_ms}")

    # -- Raw result attributes --
    print(f"\n--- All Result Attributes ---")
    for attr in sorted(dir(result)):
        if not attr.startswith("_"):
            try:
                val = getattr(result, attr)
                if not callable(val):
                    print(f"  {attr}: {val}")
            except Exception:
                pass
else:
    print("\nNo runs were returned for this job.")

# ---------------------------------------------------------------------------
# 5. Clean up
# ---------------------------------------------------------------------------
client.close()
print("\nDone.")
