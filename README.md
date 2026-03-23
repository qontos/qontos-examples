<div align="center">

<img src="assets/qontos-logo.png" alt="QONTOS" width="400">

### Examples

**Tutorials, notebooks, and integration examples for the QONTOS platform**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[Notebooks](#notebooks) &middot;
[Python Examples](#python-examples) &middot;
[Provider Examples](#provider-examples) &middot;
[Prerequisites](#prerequisites)

</div>

---

## Overview

QONTOS Examples contains hands-on notebooks, tutorials, and runnable sample programs for the QONTOS platform. It is the fastest way to learn the SDK, explore modular execution concepts, and reproduce public benchmark and simulation workflows. All examples use the public QONTOS APIs and are designed to run without access to private infrastructure.

## Prerequisites

```bash
pip install -r requirements.txt
```

During the current pre-release phase, the examples install the latest public SDK
and simulator packages directly from GitHub.

For notebook use:

```bash
pip install jupyter
```

## Notebooks

| Notebook | Topic | Qubits | Level |
|---|---|---|---|
| [01_hello_qubit.ipynb](notebooks/01_hello_qubit.ipynb) | Your first quantum circuit with QONTOS | 1 | Beginner |
| [02_bell_state.ipynb](notebooks/02_bell_state.ipynb) | Creating and measuring Bell states | 2 | Beginner |

## Python Examples

### Basic Usage

```
examples/python/
├── submit_job.py           # Submit a job to a live QONTOS API endpoint
├── circuit_normalizer.py   # Normalize circuits from different formats
├── execution_proof.py      # Generate an offline execution proof end to end
└── async_client.py         # List recent jobs with the async SDK client
```

### Partitioning

```
examples/partitioning/
├── greedy_partition.py     # Fast partitioning for small circuits
├── spectral_partition.py   # Graph-based partitioning for large circuits
```

### Provider Integration

```
examples/providers/
└── local_simulator.py      # Local Qiskit Aer simulation through qontos-sim
```

Additional provider examples will land alongside the public provider surface as
that package matures.

## Running Examples

```bash
# Run a Python example
python examples/python/submit_job.py

# Start a Jupyter notebook
jupyter notebook notebooks/
```

## Contributing

We welcome new examples. Please see the [Contributing Guide](https://github.com/qontos/.github/blob/main/CONTRIBUTING.md).

## License

[Apache License 2.0](LICENSE)

---

*Built by [Zhyra Quantum Research Institute (ZQRI)](https://zhyra.xyz) — Abu Dhabi, UAE*
