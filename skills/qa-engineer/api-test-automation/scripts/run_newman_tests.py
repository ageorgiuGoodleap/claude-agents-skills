#!/usr/bin/env python3
"""
Run Newman tests and generate HTML reports.
Usage: python run_newman_tests.py <collection_file> <environment_file>
"""
import sys
import subprocess
import json
from pathlib import Path

def run_newman(collection_path, environment_path=None, output_dir="newman_reports"):
    """Run Newman tests with HTML reporter."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    cmd = [
        "newman", "run", collection_path,
        "--reporters", "cli,html",
        "--reporter-html-export", f"{output_dir}/report.html"
    ]

    if environment_path:
        cmd.extend(["--environment", environment_path])

    print(f"Running Newman tests: {collection_path}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    print(result.stdout)
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    print(f"\n✅ Report generated: {output_dir}/report.html")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_newman_tests.py <collection_file> [environment_file]")
        sys.exit(1)

    collection = sys.argv[1]
    environment = sys.argv[2] if len(sys.argv) > 2 else None

    run_newman(collection, environment)
