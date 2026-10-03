"""E2E: real benchmark + profiler runs on real callables (PS-212).

Drives the real ``benchmark_function`` and ``profile_function`` against
in-memory callables. No network, loopback-only by construction.
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.e2e

from scitex_benchmark import BenchmarkSuite, benchmark_function, profile_function


def _work(n: int) -> int:
    return sum(range(n))


def test_benchmark_reports_nonnegative_mean() -> None:
    # Arrange
    func = _work
    # Act
    result = benchmark_function(func, args=(100,), iterations=3, warmup=1)
    # Assert
    assert result.mean_time >= 0


def test_suite_run_returns_frame() -> None:
    # Arrange
    suite = BenchmarkSuite("e2e")
    suite.add_benchmark(_work, lambda: ((10,), {}), "work", sizes=["s"])
    # Act
    frame = suite.run(iterations=2, verbose=False)
    # Assert
    assert len(frame) == 1


def test_profiled_call_returns_value() -> None:
    # Arrange
    decorated = profile_function(_work)
    # Act
    value = decorated(10)
    # Assert
    assert value == 45
