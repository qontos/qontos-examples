#!/usr/bin/env python3
# Status: works now (offline)
"""Spectral partitioning for large circuits.

The SpectralPartitioner uses the Fiedler vector of the circuit's graph
Laplacian to find a minimum-weight bisection. For more than 2 partitions
it recursively bisects the largest group.

This approach excels on larger circuits (>= 20 qubits) where greedy
expansion may get trapped in local optima.

This example:
  - Creates a 25-qubit circuit with ladder + skip topology
  - Partitions with spectral strategy
  - Inspects inter-module gates and cost evaluation
  - Compares spectral vs greedy on the same circuit

Usage:
    python spectral_partition.py
"""

from qontos.circuit import CircuitNormalizer
from qontos.partitioning import Partitioner, PartitionConstraints
from qontos.partitioning.models import (
    PartitionStrategy,
)

# ---------------------------------------------------------------------------
# 1. Programmatically build a 25-qubit ladder circuit
# ---------------------------------------------------------------------------
# A ladder topology has nearest-neighbour CX gates along a chain plus
# "rung" connections, mimicking a realistic hardware topology. At 25 qubits,
# this is large enough that spectral partitioning significantly outperforms
# greedy approaches.

NUM_QUBITS = 25

lines = [
    "OPENQASM 2.0;",
    'include "qelib1.inc";',
    f"qreg q[{NUM_QUBITS}];",
    f"creg c[{NUM_QUBITS}];",
]

# Layer 1: Hadamard on all qubits
for i in range(NUM_QUBITS):
    lines.append(f"h q[{i}];")

# Layer 2: Linear chain of CNOT gates (nearest neighbour)
for i in range(NUM_QUBITS - 1):
    lines.append(f"cx q[{i}],q[{i + 1}];")

# Layer 3: "Rung" connections every 2 qubits (skip connections)
for i in range(0, NUM_QUBITS - 2, 2):
    lines.append(f"cx q[{i}],q[{i + 2}];")

# Layer 4: Long-range skip-3 connections (creates richer connectivity)
for i in range(0, NUM_QUBITS - 3, 3):
    lines.append(f"cx q[{i}],q[{i + 3}];")

# Layer 5: Rotation layer
for i in range(NUM_QUBITS):
    lines.append(f"rz(0.5) q[{i}];")

# Layer 6: Reverse-direction chain
for i in range(NUM_QUBITS - 1, 0, -1):
    lines.append(f"cx q[{i}],q[{i - 1}];")

# Measurements
for i in range(NUM_QUBITS):
    lines.append(f"measure q[{i}] -> c[{i}];")

ladder_qasm = "\n".join(lines) + "\n"

# ---------------------------------------------------------------------------
# 2. Normalize
# ---------------------------------------------------------------------------
normalizer = CircuitNormalizer()
circuit_ir = normalizer.normalize(input_type="openqasm", source=ladder_qasm)

print("=" * 60)
print("QONTOS Spectral Partitioning Demo (25 Qubits)")
print("=" * 60)
print(f"\nCircuit: {circuit_ir.num_qubits} qubits, "
      f"{circuit_ir.gate_count} gates, depth {circuit_ir.depth}")
print(f"Connectivity edges: {len(circuit_ir.qubit_connectivity)}")

# ---------------------------------------------------------------------------
# 3. Partition into 4 modules using Spectral bisection
# ---------------------------------------------------------------------------
constraints = PartitionConstraints(
    target_partitions=4,
    preferred_strategy=PartitionStrategy.SPECTRAL,
)

partitioner = Partitioner()
plan = partitioner.run(circuit_ir, job_id="demo-spectral-25q", constraints=constraints)

# ---------------------------------------------------------------------------
# 4. Display results
# ---------------------------------------------------------------------------
print(f"\n--- Partition Plan ---")
print(f"  Strategy           : {plan.strategy}")
print(f"  Num partitions     : {plan.estimated_module_count}")
print(f"  Inter-module gates : {plan.total_inter_module_gates}")
print(f"  Balance score      : {plan.partition_balance_score:.4f}")
print(f"  Cut ratio          : {plan.cut_ratio:.4f}")
print(f"  Comm overhead (us) : {plan.estimated_communication_overhead_us:.1f}")

for entry in plan.partitions:
    print(f"\n  Partition {entry.partition_index}:")
    print(f"    Qubits (global) : {entry.qubit_indices}")
    print(f"    Num qubits      : {entry.num_qubits}")
    print(f"    Gate count      : {entry.gate_count}")
    if hasattr(entry, "inter_module_gates") and entry.inter_module_gates:
        print(f"    Inter-module    : {entry.inter_module_gates}")
    if hasattr(entry, "boundary_qubits") and entry.boundary_qubits:
        print(f"    Boundary qubits : {entry.boundary_qubits}")

# ---------------------------------------------------------------------------
# 5. Inspect inter-module gates in detail
# ---------------------------------------------------------------------------
print(f"\n--- Inter-Module Dependencies ---")
if plan.dependencies:
    for dep in plan.dependencies:
        print(f"  Partition {dep.from_partition} <-> Partition {dep.to_partition}")
        print(f"    Shared qubits  : {dep.shared_qubits}")
        print(f"    Latency (us)   : {dep.estimated_latency_us:.1f}")
else:
    print("  No inter-module dependencies.")

# ---------------------------------------------------------------------------
# 6. Cost evaluation: compare Spectral vs Greedy
# ---------------------------------------------------------------------------
print("\n--- Cost Evaluation: Spectral vs Greedy ---")

greedy_constraints = PartitionConstraints(
    target_partitions=4,
    preferred_strategy=PartitionStrategy.GREEDY,
)
greedy_plan = partitioner.run(
    circuit_ir, job_id="demo-greedy-25q", constraints=greedy_constraints,
)

print(f"  {'Metric':<28} {'Spectral':>10} {'Greedy':>10}")
print(f"  {'-' * 48}")
print(f"  {'Inter-module gates':<28} {plan.total_inter_module_gates:>10} "
      f"{greedy_plan.total_inter_module_gates:>10}")
print(f"  {'Balance score':<28} {plan.partition_balance_score:>10.4f} "
      f"{greedy_plan.partition_balance_score:>10.4f}")
print(f"  {'Cut ratio':<28} {plan.cut_ratio:>10.4f} "
      f"{greedy_plan.cut_ratio:>10.4f}")
print(f"  {'Comm overhead (us)':<28} {plan.estimated_communication_overhead_us:>10.1f} "
      f"{greedy_plan.estimated_communication_overhead_us:>10.1f}")

# Determine winner
spectral_better = plan.total_inter_module_gates <= greedy_plan.total_inter_module_gates
print(f"\n  Winner: {'Spectral' if spectral_better else 'Greedy'} "
      f"(fewer inter-module gates)")
print(f"\n  At 25 qubits, spectral partitioning typically finds a better")
print(f"  global cut because it uses the graph Laplacian to identify")
print(f"  natural community structure in the circuit connectivity.")

print("\nDone.")
