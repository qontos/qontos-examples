#!/usr/bin/env python3
"""Execute a circuit on the QONTOS local simulator.

The LocalSimulatorExecutor wraps Qiskit Aer and implements the QONTOS
ExecutorContract. It is synchronous -- submit() returns a PartitionResult
immediately.

This example shows:
  - Normalizing a circuit through CircuitNormalizer
  - Validating it against the executor's constraints
  - Running a simulation and inspecting counts

Prerequisites:
    pip install qontos qiskit-aer

Usage:
    python local_simulator.py
"""

from qontos.services.circuit_ingest.normalizer import CircuitNormalizer
from qontos.services.executor_simulator.local import LocalSimulatorExecutor

# ---------------------------------------------------------------------------
# 1. Define and normalize a circuit
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

normalizer = CircuitNormalizer()
circuit_ir = normalizer.normalize(input_type="openqasm", source=bell_qasm)

print("=" * 60)
print("QONTOS Local Simulator Demo")
print("=" * 60)
print(f"\nCircuit: {circuit_ir.num_qubits} qubits, "
      f"{circuit_ir.gate_count} gates, depth {circuit_ir.depth}")

# ---------------------------------------------------------------------------
# 2. Create the executor and validate
# ---------------------------------------------------------------------------
executor = LocalSimulatorExecutor()

print(f"\nExecutor      : {executor.provider_name}")
print(f"Synchronous   : {executor.is_synchronous}")

validation = executor.validate(circuit_ir, shots=4096)
print(f"Validation    : {'PASS' if validation.valid else 'FAIL'}")
if validation.warnings:
    for w in validation.warnings:
        print(f"  Warning: {w}")
if validation.errors:
    for e in validation.errors:
        print(f"  Error: {e}")

# ---------------------------------------------------------------------------
# 3. Execute the circuit
# ---------------------------------------------------------------------------
if validation.valid:
    print("\nRunning simulation (4096 shots)...")
    result = executor.submit(circuit_ir, shots=4096, optimization_level=1)

    print(f"\n--- Simulation Results ---")
    print(f"  Backend      : {result.backend_name}")
    print(f"  Provider     : {result.provider}")
    print(f"  Shots        : {result.shots}")
    print(f"  Elapsed (ms) : {result.elapsed_ms:.2f}")
    print(f"  Counts:")
    for bitstring, count in sorted(result.counts.items()):
        bar = "#" * int(40 * count / result.shots)
        pct = 100 * count / result.shots
        print(f"    |{bitstring}> : {count:>5}  ({pct:5.1f}%)  {bar}")

    # For a Bell state, we expect |00> and |11> each near 50%.
    total_correlated = result.counts.get("00", 0) + result.counts.get("11", 0)
    correlation_pct = 100 * total_correlated / result.shots
    print(f"\n  Correlated outcomes (|00> + |11>): {correlation_pct:.1f}%")

print("\nDone.")
