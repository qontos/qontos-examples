<div align="center">
  <a href="https://github.com/qontos">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/qontos/.github/main/assets/qontos-logo-white.png">
      <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/qontos/.github/main/assets/qontos-logo.png">
      <img src="https://raw.githubusercontent.com/qontos/.github/main/assets/qontos-logo.png" alt="QONTOS" width="260">
    </picture>
  </a>

  <h3>QONTOS Examples</h3>
  <p><strong>Runnable notebooks, workflows, and adoption paths for the QONTOS platform.</strong></p>
  <p>The public learning surface for circuit ingestion, partitioning, simulation, proofs, and provider interoperability.</p>

  <p>
    <img src="https://img.shields.io/badge/Visibility-Public-0f766e?style=flat-square" alt="Visibility: Public">
    <img src="https://img.shields.io/badge/Track-Examples-0b3b8f?style=flat-square" alt="Track: Examples">
    <img src="https://img.shields.io/badge/Status-Pre--release-c2410c?style=flat-square" alt="Status: Pre-release">
  </p>

  <p>
    <a href="#overview">Overview</a> &middot;
    <a href="#start-here">Start Here</a> &middot;
    <a href="#installation">Installation</a> &middot;
    <a href="#repository-map">Repository Map</a> &middot;
    <a href="#execution-modes">Execution Modes</a> &middot;
    <a href="#related-repositories">Related Repositories</a>
  </p>
</div>

---

## Overview

QONTOS Examples is the public adoption layer for the QONTOS stack. It turns the SDK, simulator, and benchmark concepts into runnable notebooks and scripts that show how the platform behaves in real workflows.

## Start Here

| Level | Resource | Description |
| --- | --- | --- |
| Beginner | [Hello Qubit](notebooks/01_hello_qubit.ipynb) | First circuit submission and result inspection |
| Beginner | [Bell State](notebooks/02_bell_state.ipynb) | Entanglement and measurement basics |
| Intermediate | [Partitioning](notebooks/03_partitioning.ipynb) | Modular execution planning for larger circuits |
| Intermediate | [Multi-Backend](notebooks/04_multi_backend.ipynb) | Registry-driven backend selection and scheduling |
| Advanced | [VQE Chemistry](notebooks/05_vqe_h2.ipynb) | Hybrid chemistry-style workflow with QONTOS primitives |

## Installation

Python 3.10 or later is required.

### Pre-release (current)

The QONTOS packages are not yet published to PyPI. Install from pinned release tags:

```bash
pip install git+https://github.com/qontos/qontos.git@v0.2.0
pip install git+https://github.com/qontos/qontos-sim.git@v0.1.0
```

Or install the curated examples environment:

```bash
pip install -r requirements.txt
```

> **Note**: Once packages are published to PyPI, installation will simplify to `pip install qontos qontos-sim`.

## Repository Map

| Path | Purpose |
| --- | --- |
| `notebooks/` | Guided notebook walkthroughs from beginner to advanced workflows |
| `examples/python/` | Core SDK and proof-oriented scripts |
| `examples/partitioning/` | Partitioning strategy examples and algorithm comparisons |
| `examples/providers/` | Local simulator, provider-specific, and future native-hardware examples |
| `tests/` | Lightweight checks that keep examples aligned with the public API surface |

## Example Catalog

### Core SDK

- [`submit_job.py`](examples/python/submit_job.py) - basic job submission flow
- [`async_jobs.py`](examples/python/async_jobs.py) - async multi-job workflow
- [`execution_proof.py`](examples/python/execution_proof.py) - execution integrity walkthrough
- [`result_inspection.py`](examples/python/result_inspection.py) - result analysis and inspection
- [`circuit_normalization.py`](examples/python/circuit_normalization.py) - ingest and normalize circuits offline

### Partitioning

- [`greedy_partition.py`](examples/partitioning/greedy_partition.py) - simple modular partitioning
- [`spectral_partition.py`](examples/partitioning/spectral_partition.py) - larger graph-based partitioning path

### Providers

- [`local_simulator.py`](examples/providers/local_simulator.py) - local simulator execution
- [`ibm_quantum.py`](examples/providers/ibm_quantum.py) - IBM Quantum integration path
- [`amazon_braket.py`](examples/providers/amazon_braket.py) - Amazon Braket integration path
- [`native_qontos.py`](examples/providers/native_qontos.py) - future native hardware interface shape

## Execution Modes

| Example | Status | Requirements |
| --- | --- | --- |
| `circuit_normalization.py` | Works now | Offline |
| `submit_job.py` | Works now | Local simulator |
| `execution_proof.py` | Works now | Offline |
| `greedy_partition.py` | Works now | Offline |
| `spectral_partition.py` | Works now | Offline |
| `local_simulator.py` | Works now | Local simulator |
| `async_jobs.py` | Requires server | Running QONTOS API |
| `result_inspection.py` | Requires server | Running QONTOS API |
| `ibm_quantum.py` | Requires credentials | IBM Quantum account |
| `amazon_braket.py` | Requires credentials | AWS account |
| `native_qontos.py` | Future path | Native hardware in development |

## Related Repositories

| Repository | Role |
| --- | --- |
| [qontos](https://github.com/qontos/qontos) | Flagship SDK and public developer entry point |
| [qontos-sim](https://github.com/qontos/qontos-sim) | Simulators, digital twin, and tensor-network modeling |
| [qontos-benchmarks](https://github.com/qontos/qontos-benchmarks) | Evidence and methodology for public claims |
| [qontos-research](https://github.com/qontos/qontos-research) | Whitepapers, roadmap, and technical publications |

---

<p align="center">
  <sub>QONTOS · Hybrid superconducting-photonic quantum computing · Built by Zhyra Quantum Research Institute (ZQRI)</sub>
</p>
