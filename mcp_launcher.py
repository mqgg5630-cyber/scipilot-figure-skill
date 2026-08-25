"""Dependency bootstrap and cross-platform launcher for the local MCP server."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV = ROOT / ".venv"
VENV_PYTHON = VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def _run(command: list[str]) -> None:
    # stdout is reserved for MCP JSON-RPC when Antigravity starts this launcher.
    subprocess.run(command, cwd=ROOT, check=True, stdout=sys.stderr)


def ensure_environment() -> Path:
    """Create the repo-local virtualenv and install dependencies when needed."""
    if not VENV_PYTHON.exists():
        print("SciPilot MCP: creating .venv ...", file=sys.stderr)
        _run([sys.executable, "-m", "venv", str(VENV)])

    probe = subprocess.run(
        [str(VENV_PYTHON), "-c", "import mcp, pandas, matplotlib, PIL"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if probe.returncode != 0:
        print("SciPilot MCP: installing dependencies ...", file=sys.stderr)
        _run(
            [
                str(VENV_PYTHON),
                "-m",
                "pip",
                "install",
                "-r",
                str(ROOT / "requirements.txt"),
            ]
        )
    return VENV_PYTHON


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepare and launch the SciPilot Figure stdio MCP server."
    )
    parser.add_argument(
        "--setup-only",
        action="store_true",
        help="prepare .venv and dependencies without starting the MCP server",
    )
    args = parser.parse_args()
    python = ensure_environment()
    if args.setup_only:
        print(f"SciPilot MCP environment ready: {python}")
        return
    os.execv(str(python), [str(python), str(ROOT / "mcp_server.py")])


if __name__ == "__main__":
    main()
