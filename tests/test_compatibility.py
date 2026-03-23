"""Cross-repo compatibility smoke tests.

Verifies that the QONTOS SDK, simulator, and examples all work together
using the same API contract. This catches drift between repos before it
reaches users.
"""

import importlib
import inspect
import subprocess
import sys

import pytest


class TestCrossRepoImports:
    """Verify all three packages can be imported together."""

    def test_sdk_imports(self):
        import qontos
        assert hasattr(qontos, "__version__")

    def test_simulator_imports(self):
        import qontos_sim
        assert hasattr(qontos_sim, "__version__")

    def test_cross_package_types(self):
        """SDK types used by simulator are compatible."""
        from qontos.models.circuit import CircuitIR
        from qontos.models.result import PartitionResult
        # These types must be importable from both sides
        assert CircuitIR is not None
        assert PartitionResult is not None

    def test_simulator_uses_sdk_types(self):
        """LocalSimulatorExecutor accepts CircuitIR from SDK."""
        from qontos.models.circuit import CircuitIR
        from qontos_sim.local import LocalSimulatorExecutor
        sig = inspect.signature(LocalSimulatorExecutor.submit)
        params = sig.parameters
        # First param after self should accept CircuitIR
        assert "circuit_ir" in params


class TestAPIContractAlignment:
    """Verify example code matches the actual SDK API."""

    def test_submit_job_has_constraints(self):
        """submit_job must accept 'constraints' (used by provider examples)."""
        from qontos import QontosClient
        sig = inspect.signature(QontosClient.submit_job)
        assert "constraints" in sig.parameters

    def test_submit_job_no_backend_config(self):
        """submit_job must NOT have 'backend_config' (was a bug)."""
        from qontos import QontosClient
        sig = inspect.signature(QontosClient.submit_job)
        assert "backend_config" not in sig.parameters

    def test_submit_job_has_name(self):
        from qontos import QontosClient
        sig = inspect.signature(QontosClient.submit_job)
        assert "name" in sig.parameters

    def test_submit_job_has_tags(self):
        from qontos import QontosClient
        sig = inspect.signature(QontosClient.submit_job)
        assert "tags" in sig.parameters


class TestOfflineExamples:
    """Verify offline examples can at least be imported without errors."""

    OFFLINE_EXAMPLES = [
        "examples/python/circuit_normalization.py",
        "examples/python/execution_proof.py",
        "examples/partitioning/greedy_partition.py",
        "examples/partitioning/spectral_partition.py",
    ]

    LOCAL_SIMULATOR_EXAMPLES = [
        "examples/providers/local_simulator.py",
    ]

    ALL_RUNNABLE = OFFLINE_EXAMPLES + LOCAL_SIMULATOR_EXAMPLES

    @pytest.mark.parametrize("example_path", OFFLINE_EXAMPLES + LOCAL_SIMULATOR_EXAMPLES)
    def test_example_importable(self, example_path):
        """Example module can be imported (syntax check)."""
        result = subprocess.run(
            [sys.executable, "-c", f"import ast; ast.parse(open('{example_path}').read())"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Syntax error in {example_path}: {result.stderr}"

    @pytest.mark.parametrize("example_path", OFFLINE_EXAMPLES)
    def test_offline_example_runs(self, example_path):
        """Offline example runs successfully without network or server."""
        result = subprocess.run(
            [sys.executable, example_path],
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, (
            f"Offline example {example_path} failed:\n{result.stderr}"
        )
