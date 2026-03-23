#!/usr/bin/env python3
"""Generate an execution proof for a local, single-partition workflow.

This example stays fully offline. It walks through the same logical stages the
platform uses in production: circuit ingest, partition planning, result
aggregation, and proof generation.
"""

from qontos.circuit.normalizer import CircuitNormalizer
from qontos.integrity import ProofGenerator
from qontos.models import PartitionResult
from qontos.partitioning import PartitionConstraints, Partitioner
from qontos.results import ResultAggregator

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
circuit_ir, manifest = normalizer.normalize_to_manifest(
    input_type="openqasm",
    source=bell_qasm,
    user_id="demo-user",
    name="Bell Proof Demo",
)

plan = Partitioner().run(
    circuit_ir,
    job_id=manifest.job_id,
    constraints=PartitionConstraints(target_partitions=1),
)

partition_result = PartitionResult(
    partition_id=plan.partitions[0].partition_id,
    partition_index=0,
    backend_id="local-simulator",
    backend_name="aer_simulator",
    provider="simulator",
    counts={"00": 512, "11": 512},
    shots_completed=1024,
    execution_time_ms=3.2,
    metadata={"source": "qontos-examples"},
)

run_result = ResultAggregator().aggregate(
    manifest.job_id,
    [partition_result],
    plan,
)
proof = ProofGenerator().generate(manifest, plan, run_result)

print("QONTOS Execution Proof Demo")
print("=" * 60)
print(f"Job ID           : {manifest.job_id}")
print(f"Circuit hash     : {manifest.circuit_hash[:16]}...")
print(f"Plan strategy    : {plan.strategy}")
print(f"Final counts     : {run_result.final_counts}")
print(f"Proof hash       : {proof.proof_hash}")
print(f"Input digest     : {proof.input_digest}")
print(f"Execution digest : {proof.execution_digest}")
print(f"Output digest    : {proof.output_digest}")
