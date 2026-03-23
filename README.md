# QONTOS Examples

Hands-on tutorials and runnable examples for the QONTOS quantum computing platform.

## Start Here

| Level | Resource | Description |
|-------|----------|-------------|
| Beginner | [Hello Qubit](notebooks/01_hello_qubit.ipynb) | Your first quantum circuit with QONTOS |
| Beginner | [Bell State](notebooks/02_bell_state.ipynb) | Create and measure entanglement |
| Intermediate | [Partitioning](notebooks/03_partitioning.ipynb) | Split circuits across modules |
| Intermediate | [Multi-Backend](notebooks/04_multi_backend.ipynb) | Schedule across providers |
| Advanced | [VQE Chemistry](notebooks/05_vqe_h2.ipynb) | H2 ground state estimation |

## Python Examples

### Core SDK
- [`submit_job.py`](examples/python/submit_job.py) — Basic job submission
- [`async_jobs.py`](examples/python/async_jobs.py) — Async multi-job workflow
- [`execution_proof.py`](examples/python/execution_proof.py) — Integrity verification
- [`result_inspection.py`](examples/python/result_inspection.py) — Deep result analysis

### Partitioning
- [`greedy_partition.py`](examples/partitioning/greedy_partition.py) — Small circuit partitioning
- [`spectral_partition.py`](examples/partitioning/spectral_partition.py) — Large circuit partitioning

### Providers
- [`local_simulator.py`](examples/providers/local_simulator.py) — Local simulator execution
- [`ibm_quantum.py`](examples/providers/ibm_quantum.py) — IBM Quantum (requires credentials)
- [`amazon_braket.py`](examples/providers/amazon_braket.py) — Amazon Braket (requires credentials)
- [`native_qontos.py`](examples/providers/native_qontos.py) — Future native hardware path

## Prerequisites

- Python >= 3.10
- `pip install qontos` (SDK)
- `pip install qontos-sim` (for local simulator examples)
- No quantum hardware access needed for most examples

## Related Repositories

- [qontos](https://github.com/qontos/qontos) — Flagship SDK
- [qontos-sim](https://github.com/qontos/qontos-sim) — Simulators
- [qontos-benchmarks](https://github.com/qontos/qontos-benchmarks) — Benchmarks
- [qontos-research](https://github.com/qontos/qontos-research) — Research papers
