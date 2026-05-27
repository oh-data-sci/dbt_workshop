#!/usr/bin/env python3
"""
Instructor-only script: rebuilds data/otb.duckdb from raw CSVs.

Usage (from repo root):
    uv run python scripts/build_otb_duckdb.py

Prerequisites:
    - data/raw/airport-codes.csv        (~8.8 MB)
    - data/raw/onthebeachexport.csv     (~242 MB)

This script is NOT part of the participant workflow. Participants receive
otb.duckdb as a pre-built GitHub Release asset (see main.py prep).

After running, publish the new file as a GitHub Release asset:
    gh release create workshop-data-v1 data/otb.duckdb \\
        --title "Workshop data v1" \\
        --notes "Pre-built DuckDB warehouse for dbt-in-1-2-3 workshop"

Then record the release URL and SHA-256 checksum in main.py.
"""

import hashlib
import sys
from pathlib import Path

import duckdb

REPO_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = REPO_ROOT / "data" / "otb.duckdb"
AIRPORTS_CSV = REPO_ROOT / "data" / "raw" / "airport-codes.csv"
PRICES_CSV = REPO_ROOT / "data" / "raw" / "onthebeachexport.csv"


def check_sources() -> None:
    missing = [p for p in (AIRPORTS_CSV, PRICES_CSV) if not p.exists()]
    if missing:
        for p in missing:
            print(f"ERROR: missing source file: {p}", file=sys.stderr)
        sys.exit(1)


def build(db_path: Path = DB_PATH) -> None:
    check_sources()

    print(f"Building {db_path} ...")
    db_path.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(db_path))

    print("  Creating raw schema ...")
    con.execute("CREATE SCHEMA IF NOT EXISTS raw")

    print(f"  Loading raw.airports from {AIRPORTS_CSV.name} ...")
    con.execute("DROP TABLE IF EXISTS raw.airports")
    con.execute(
        f"CREATE TABLE raw.airports AS SELECT * FROM read_csv_auto('{AIRPORTS_CSV}')"
    )
    airport_count = con.execute("SELECT COUNT(*) FROM raw.airports").fetchone()[0]
    print(f"    → {airport_count:,} rows")

    print(f"  Loading raw.prices from {PRICES_CSV.name} ...")
    con.execute("DROP TABLE IF EXISTS raw.prices")
    con.execute(
        f"CREATE TABLE raw.prices AS SELECT * FROM read_csv_auto('{PRICES_CSV}')"
    )
    price_count = con.execute("SELECT COUNT(*) FROM raw.prices").fetchone()[0]
    print(f"    → {price_count:,} rows")

    con.close()

    # Print checksum for pasting into main.py
    sha256 = hashlib.sha256(db_path.read_bytes()).hexdigest()
    print(f"\nDone. SHA-256: {sha256}")
    print(f"\nNext steps:")
    print(f"  1. Publish: gh release create workshop-data-v1 {db_path} \\")
    print(f'         --title "Workshop data v1"')
    print(f"  2. Paste the release asset URL and SHA-256 above into main.py")


if __name__ == "__main__":
    build()
