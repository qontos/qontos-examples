#!/usr/bin/env python3
# Status: works now (offline)
"""Normalize quantum circuits with QONTOS CircuitNormalizer.

Shows how QONTOS converts raw OpenQASM into a provider-agnostic
CircuitIR, extracting structural metadata along the way.

The normalizer is the entry point to the entire QONTOS pipeline --
every circuit passes through it before partitioning or execution.

Usage:
    python circuit_normalization.py
"""

from qontos.circuit import CircuitNormalizer
from qontos.circuit.metadata import extract_metadata

# ---------------------------------------------------------------------------
# 1. Create the normalizer
# ---------------------------------------------------------------------------
normalizer = CircuitNormalizer()

# ---------------------------------------------------------------------------
# 2. Define circuits of increasing complexity
# ---------------------------------------------------------------------------

# Simple single-qubit Hadamard + measure
hadamard_qasm = """\
OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
creg c[1];
h q[0];
measure q[0] -> c[0];
"""

# Two-qubit Bell state
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

# Three-qubit GHZ state
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

circuits = {
    "Hadamard (1Q)": hadamard_qasm,
    "Bell State (2Q)": bell_qasm,
    "GHZ-3 (3Q)": ghz3_qasm,
}

# ---------------------------------------------------------------------------
# 3. Normalize each circuit and display metadata
# ---------------------------------------------------------------------------
print("=" * 60)
print("QONTOS Circuit Normalization Demo")
print("=" * 60)

for name, qasm in circuits.items():
    print(f"\n--- {name} ---")

    # Normalize: QASM string -> CircuitIR
    circuit_ir = normalizer.normalize(input_type="openqasm", source=qasm)

    # Extract rich metadata
    metadata = extract_metadata(circuit_ir)

    # Display core properties
    print(f"  Qubits          : {circuit_ir.num_qubits}")
    print(f"  Classical bits  : {circuit_ir.num_clbits}")
    print(f"  Circuit depth   : {circuit_ir.depth}")
    print(f"  Gate count      : {circuit_ir.gate_count}")
    print(f"  Circuit hash    : {circuit_ir.circuit_hash[:16]}...")

    # Display extracted metadata
    print(f"  1Q gates        : {metadata['single_qubit_gates']}")
    print(f"  2Q gates        : {metadata['two_qubit_gates']}")
    print(f"  Entanglement    : {metadata['entanglement_density']:.4f}")
    print(f"  Parallelism     : {metadata['parallelism_ratio']:.4f}")
    print(f"  Gate types      : {metadata['gate_type_distribution']}")
    print(f"  Has measurements: {metadata['has_measurements']}")

print("\n" + "=" * 60)
print("All circuits normalized successfully.")
