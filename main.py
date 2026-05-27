#!/usr/bin/env python3
"""
Workshop orchestration script.

Usage:
    python main.py prep     # Download and verify data/otb.duckdb
    python main.py debug    # Run dbt debug from dbt_in_123/
    python main.py build    # Run dbt seed && dbt run && dbt test
"""

import hashlib
import subprocess
import sys
from pathlib import Path

import httpx

# ---------------------------------------------------------------------------
# Release configuration
# TODO: After publishing the GitHub Release, replace these two values.
#   1. Run: python scripts/build_otb_duckdb.py  (prints the SHA-256)
#   2. Publish: gh release create workshop-data-v1 data/otb.duckdb \
#                   --title "Workshop data v1"
#   3. Copy the asset URL from the release page (or gh release view) and
#      paste it below.
# ---------------------------------------------------------------------------
RELEASE_URL = (
    # TODO: replace with the actual GitHub Release asset URL, e.g.:
    # "https://github.com/oh-data-sci/dbt_workshop/releases/download/workshop-data-v1/otb.duckdb"
    "TODO"
)
EXPECTED_SHA256 = (
    # TODO: replace with the hex digest printed by scripts/build_otb_duckdb.py
    "TODO"
)
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent
DB_PATH = REPO_ROOT / "data" / "otb.duckdb"
DBT_DIR = REPO_ROOT / "dbt_in_123"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def run_dbt(*args: str) -> None:
    """Run a dbt command from the dbt_in_123/ directory."""
    cmd = ["dbt", *args]
    result = subprocess.run(cmd, cwd=DBT_DIR)
    sys.exit(result.returncode)


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------

def cmd_prep() -> None:
    """Download and verify data/otb.duckdb (idempotent)."""
    if RELEASE_URL == "TODO" or EXPECTED_SHA256 == "TODO":
        print(
            "ERROR: Release URL and SHA-256 have not been set in main.py.\n"
            "Run scripts/build_otb_duckdb.py, publish a GitHub Release, then\n"
            "update RELEASE_URL and EXPECTED_SHA256 at the top of main.py.",
            file=sys.stderr,
        )
        sys.exit(1)

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Idempotency check: skip download if file is already present and intact
    if DB_PATH.exists():
        existing = sha256_of(DB_PATH)
        if existing == EXPECTED_SHA256:
            print(f"data/otb.duckdb is already present and verified. Nothing to do.")
            return
        else:
            print(
                f"WARNING: data/otb.duckdb exists but checksum mismatch "
                f"(expected {EXPECTED_SHA256[:12]}…, got {existing[:12]}…). "
                f"Re-downloading."
            )

    print(f"Downloading otb.duckdb from GitHub Release ...")
    tmp_path = DB_PATH.with_suffix(".duckdb.tmp")
    try:
        with httpx.stream("GET", RELEASE_URL, follow_redirects=True) as r:
            r.raise_for_status()
            total = int(r.headers.get("content-length", 0))
            downloaded = 0
            with open(tmp_path, "wb") as f:
                for chunk in r.iter_bytes(chunk_size=65536):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        pct = downloaded / total * 100
                        print(f"  {pct:5.1f}%  ({downloaded:,} / {total:,} bytes)", end="\r")
        print()

        # Verify checksum before replacing the target file
        actual = sha256_of(tmp_path)
        if actual != EXPECTED_SHA256:
            tmp_path.unlink(missing_ok=True)
            print(
                f"ERROR: Checksum mismatch!\n"
                f"  Expected: {EXPECTED_SHA256}\n"
                f"  Got:      {actual}\n"
                "The downloaded file has been discarded. "
                "Check that RELEASE_URL and EXPECTED_SHA256 in main.py are correct.",
                file=sys.stderr,
            )
            sys.exit(1)

        tmp_path.replace(DB_PATH)
        print(f"data/otb.duckdb downloaded and verified ({DB_PATH.stat().st_size:,} bytes).")

    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise


def cmd_debug() -> None:
    """Dispatch to dbt debug from dbt_in_123/."""
    run_dbt("debug")


def cmd_build() -> None:
    """Dispatch to dbt seed && dbt run && dbt test from dbt_in_123/."""
    for step in ("seed", "run", "test"):
        result = subprocess.run(["dbt", step], cwd=DBT_DIR)
        if result.returncode != 0:
            sys.exit(result.returncode)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

COMMANDS = {
    "prep": cmd_prep,
    "debug": cmd_debug,
    "build": cmd_build,
}


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in COMMANDS:
        print(
            f"Usage: python main.py <command>\n"
            f"Commands: {', '.join(COMMANDS)}",
            file=sys.stderr,
        )
        sys.exit(1)
    COMMANDS[sys.argv[1]]()


if __name__ == "__main__":
    main()
