import subprocess
import sys
from pathlib import Path

from codegen.utils import ROOT


def run_ruff(target: Path) -> None:
    """Run ruff check (fix unused imports) and format on a target path.

    :param target: path to the file or directory to lint and format.
    """
    print(f"Running ruff check on {target.name}/...")
    result = subprocess.run(
        [
            sys.executable, "-m", "ruff", "check", str(target),
            "--select", "F401,I", "--fix", "--quiet",
        ],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    if result.returncode != 0:
        print(f"Ruff check failed:\n{result.stderr}")

    print(f"Running ruff format on {target.name}/...")
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "format", str(target), "--quiet"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    if result.returncode != 0:
        print(f"Ruff format failed:\n{result.stderr}")
