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
pip install qontos
pip install jupyter  # for notebooks
```

For provider-specific examples:

```bash
pip install "qontos[ibm]"      # IBM Quantum
pip install "qontos[braket]"   # Amazon Braket
pip install "qontos[all]"      # Everything
```

## Notebooks

| Notebook | Topic | Qubits | Level |
|---|---|---|---|
| [01_hello_qubit.ipynb](notebooks/01_hello_qubit.ipynb) | Your first quantum circuit with QONTOS | 1 | Beginner |
| [02_bell_state.ipynb](notebooks/02_bell_state.ipynb) | Creating and measuring Bell states | 2 | Beginner |
| [03_circuit_partitioning.ipynb](notebooks/03_circuit_partitioning.ipynb) | Partitioning circuits for modular execution | 5-10 | Intermediate |
| [04_multi_backend.ipynb](notebooks/04_multi_backend.ipynb) | Running across IBM Quantum and simulators | 3-5 | Intermediate |
| [05_vqe_chemistry.ipynb](notebooks/05_vqe_chemistry.ipynb) | Variational quantum eigensolver for H2 | 2-4 | Advanced |

## Python Examples

### Basic Usage

```
examples/python/
├── submit_job.py           # Submit a circuit and get results
├── circuit_normalizer.py   # Normalize circuits from different formats
├── execution_proof.py      # Generate and verify execution proofs
└── async_client.py         # Asynchronous job submission
```

### Partitioning

```
examples/partitioning/
├── greedy_partition.py     # Fast partitioning for small circuits
├── spectral_partition.py   # Graph-based partitioning for large circuits
├── manual_partition.py     # User-specified qubit-to-module mapping
└── partition_analysis.py   # Analyze partition quality metrics
```

### Provider Integration

```
examples/providers/
├── ibm_quantum.py          # IBM Quantum backend execution
├── amazon_braket.py        # Amazon Braket backend execution
├── local_simulator.py      # Qiskit Aer local simulation
└── custom_executor.py      # Building a custom backend executor
```

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
