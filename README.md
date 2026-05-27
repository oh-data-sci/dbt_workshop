dbt in 1-2-3
===

A 2-hour, in-person beginner workshop introducing [dbt](https://docs.getdbt.com/) to SQL-literate analysts. We use a local DuckDB database containing real travel-pricing data — a dataset deliberately too large for Excel, which is exactly the point.

## The data

The workshop database (`otb.duckdb`) contains two tables in the `raw` schema:

| Table | Rows | Description |
|---|---|---|
| `raw.airports` | ~85,000 | Airport reference data (name, IATA/ICAO codes, country, coordinates) |
| `raw.prices` | ~1,085,000 | On The Beach holiday-pricing export: packages, hotels, flights, prices |

The two tables join on `prices.arrival_airport_code = airports.iata_code`.

Two small reference tables are loaded via `dbt seed`:

| Seed | Rows | Description |
|---|---|---|
| `country_codes_regions` | ~249 | ISO 3166-1 country codes with region/sub-region |
| `geo_calling_codes` | ~195 | Country calling codes |

## Prerequisites

You need the following on your laptop before the workshop starts:

### macOS

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install DuckDB CLI (for ad-hoc queries)
brew install duckdb
```

### Windows (PowerShell)

```powershell
# Install uv
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install DuckDB CLI — download from https://duckdb.org/docs/installation/
```

### Linux (Ubuntu/Debian)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install DuckDB CLI
curl -L https://github.com/duckdb/duckdb/releases/latest/download/duckdb_cli-linux-amd64.zip \
  -o /tmp/duckdb.zip && unzip /tmp/duckdb.zip -d ~/.local/bin
```

## Getting started

```bash
# 1. Clone the repo
git clone https://github.com/oh-data-sci/dbt_workshop.git
cd dbt_workshop

# 2. Install Python dependencies
uv sync

# 3. Download the workshop database (~42 MB)
python main.py prep

# 4. Configure your dbt profile
cp dbt_in_123/profiles.example.yml ~/.dbt/profiles.yml

# 5. Verify everything works
cd dbt_in_123
dbt debug          # → "All checks passed!"
dbt seed           # loads country_codes_regions + geo_calling_codes
```

### Workshop database

`otb.duckdb` is hosted as a GitHub Release asset. `python main.py prep` downloads it automatically and verifies the SHA-256 checksum. Run it before the session — conference wifi can be slow.

Direct download (if needed):
[https://github.com/oh-data-sci/dbt_workshop/releases/tag/workshop-data-v1](https://github.com/oh-data-sci/dbt_workshop/releases/tag/workshop-data-v1)

## Running the workshop pipeline

```bash
python main.py prep     # download + verify data/otb.duckdb (idempotent)
python main.py debug    # dbt debug
python main.py build    # dbt seed && dbt run && dbt test
```

## Lessons

| File | Topic | Duration |
|---|---|---|
| `lessons/01_setup.md` | Project setup, dbt debug, first seed load | ~30 min |
| `lessons/02a_cleaning.md` | Cleaning models — types, nulls, dates | ~30 min |
| `lessons/02b_joining.md` | Joining cleaned tables | ~20 min |
| `lessons/03_data_products_semantics.md` | Analytical aggregations | ~30 min |

## Optional: cloud target via MotherDuck

If you want to run the workshop against a cloud DuckDB instance instead of a local file:

1. Sign up for a free account at [https://motherduck.com](https://motherduck.com)
2. Create a token at [https://app.motherduck.com/settings/tokens](https://app.motherduck.com/settings/tokens)
3. Export your token: `export MOTHERDUCK_TOKEN=<your-token>`
4. In `~/.dbt/profiles.yml`, uncomment and switch to the `motherduck` output:

```yaml
dbt_in_123:
  target: motherduck
  outputs:
    motherduck:
      type: duckdb
      path: "md:dbt_workshop"
      token: "{{ env_var('MOTHERDUCK_TOKEN') }}"
      threads: 4
```

The MotherDuck path is entirely optional — the local DuckDB file is the default and recommended setup for the workshop.

## Project structure

```
dbt_workshop/
  ├── data/                       # gitignored; populated by python main.py prep
  │   └── otb.duckdb              # workshop database (~42 MB)
  ├── dbt_in_123/                 # the dbt project
  │   ├── models/
  │   │   ├── sources.yml         # raw layer source declarations
  │   │   └── otb/                # domain models (added during lessons)
  │   ├── seeds/
  │   │   ├── country_codes_regions.csv
  │   │   └── geo_calling_codes.csv
  │   ├── profiles.example.yml    # copy to ~/.dbt/profiles.yml
  │   └── dbt_project.yml
  ├── lessons/                    # participant instruction files
  ├── scripts/
  │   └── build_otb_duckdb.py     # instructor-only: rebuild DB from raw CSVs
  ├── sql/                        # instructor-only: raw load scripts
  ├── main.py                     # workshop runner
  └── pyproject.toml
```
