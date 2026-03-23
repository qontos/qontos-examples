#!/usr/bin/env python3
"""Partition a quantum circuit using the Greedy strategy.

The GreedyPartitioner grows partitions outward from high-degree seed
qubits, producing balanced partitions that minimize inter-module gates.
It works well for small-to-medium circuits (< 20 qubits).

Usage:
    python greedy_partition.py
"""

from qontos.circuit import CircuitNormalizer
from qontos.partitioning import Partitioner, PartitionConstraints
from qontos.partitioning.models import (
    PartitionStrategy,
)

# ---------------------------------------------------------------------------
# 1. Build a 6-qubit circuit with interesting connectivity
# ---------------------------------------------------------------------------
# This circuit has a mix of nearest-neighbour and long-range gates,
# making it a good candidate for demonstrating partitioning quality.
qasm_6q = """\
OPENQASM 2.0;
include "qelib1.inc";
qreg q[6];
creg c[6];
h q[0];
h q[3];
cx q[0],q[1];
cx q[1],q[2];
cx q[3],q[4];
cx q[4],q[5];
cx q[2],q[3];
h q[1];
h q[4];
cx q[0],q[5];
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
measure q[3] -> c[3];
measure q[4] -> c[4];
measure q[5] -> c[5];
"""

# ---------------------------------------------------------------------------
# 2. Normalize the circuit
# ---------------------------------------------------------------------------
normalizer = CircuitNormalizer()
circuit_ir = normalizer.normalize(input_type="openqasm", source=qasm_6q)

print("=" * 60)
print("QONTOS Greedy Partitioning Demo")
print("=" * 60)
print(f"\nCircuit: {circuit_ir.num_qubits} qubits, "
      f"{circuit_ir.gate_count} gates, depth {circuit_ir.depth}")
print(f"Connectivity edges: {circuit_ir.qubit_connectivity}")

# ---------------------------------------------------------------------------
# 3. Partition into 2 modules using the Greedy strategy
# ---------------------------------------------------------------------------
constraints = PartitionConstraints(
    target_partitions=2,
    preferred_strategy=PartitionStrategy.GREEDY,
)

partitioner = Partitioner()
plan = partitioner.run(circuit_ir, job_id="demo-greedy", constraints=constraints)

# ---------------------------------------------------------------------------
# 4. Inspect the partition plan
# ---------------------------------------------------------------------------
print(f"\n--- Partition Plan ---")
print(f"  Strategy         : {plan.strategy}")
print(f"  Num partitions   : {plan.estimated_module_count}")
print(f"  Inter-module gates: {plan.total_inter_module_gates}")
print(f"  Balance score    : {plan.partition_balance_score:.4f}")
print(f"  Cut ratio        : {plan.cut_ratio:.4f}")
print(f"  Comm overhead (us): {plan.estimated_communication_overhead_us:.1f}")

for entry in plan.partitions:
    print(f"\n  Partition {entry.partition_index}:")
    print(f"    ID              : {entry.partition_id}")
    print(f"    Qubits (global) : {entry.qubit_indices}")
    print(f"    Num qubits      : {entry.num_qubits}")
    print(f"    Gate count      : {entry.gate_count}")
    print(f"    Qubit mapping   : {entry.qubit_mapping}")

if plan.dependencies:
    print(f"\n  Dependencies:")
    for dep in plan.dependencies:
        print(f"    {dep.from_partition} <-> {dep.to_partition}")
        print(f"      Shared qubits : {dep.shared_qubits}")
        print(f"      Latency (us)  : {dep.estimated_latency_us:.1f}")

print("\nDone.")
