"""Smoke: installed package imports and times one callable (PS-211).

Subprocess-driven (``sys.executable -c ...``) so this proves the installed
distribution resolves — an in-process import would not. Hermetic: no
network, no credentials, no writes outside tmp dirs.
"""

from __future__ import annotations

import subprocess
import sys

import pytest

pytestmark = pytest.mark.smoke


def test_import_and_benchmark_subprocess() -> None:
    # Arrange
    argv = [
        sys.executable,
        "-c",
        "import scitex_benchmark as sb; "
        "r = sb.benchmark_function(sum, args=([1, 2, 3],), iterations=3, warmup=1); "
        "print(r.mean_time >= 0)",
    ]
    # Act
    completed = subprocess.run(argv, capture_output=True, text=True, timeout=60)
    # Assert
    assert (completed.returncode, completed.stdout.strip()) == (0, "True")
