# Change: Add Workshop Foundations

## Why

The `dbt-in-1-2-3` workshop needs a stable, reproducible starting point before any lesson content can be authored. Today the repo holds only `dbt init` scaffolding, a 0-byte placeholder `data/raw.duckdb`, divergent uncommitted local work in the main worktree, and `dbt_project.yml` that doesn't parse cleanly — nothing builds end-to-end.

The chosen dataset (On The Beach holiday-pricing export + airport reference data; ~1 M + 85 K rows) is a deliberate teaching choice: it is large enough that Excel would struggle, which motivates dbt and SQL warehousing for the workshop's Excel-leaning beginner audience.

This change establishes the foundations layer: the raw DuckDB warehouse, a clean dbt project skeleton, source declarations, reference seeds, a portable profile template, an orchestration script, and accurate root-level documentation. After this change lands, every subsequent lesson change (01–03) builds on a working `dbt debug` / `dbt seed` / `dbt parse` baseline.

## What Changes

- Establish `data/otb.duckdb` (gitignored) as the canonical raw warehouse, fetched via `python main.py prep` from a GitHub Release asset.
- Promote `sql/load_raw_*.sql` to a fixed, idempotent instructor-only build path (`scripts/build_otb_duckdb.py`); separate `CREATE TABLE` from exploratory queries; fix the broken `COUNT(DISTINCT )` line in `load_raw_airports.sql`.
- Rewrite `dbt_in_123/dbt_project.yml`: project/profile key `dbt_in_123`, point models at `models/otb/`, default materialization `view`, configure `seeds/`.
- Add `dbt_in_123/models/sources.yml` declaring source `otb_raw` (schema `raw`) with tables `airports` and `prices` and their columns.
- Add `dbt_in_123/seeds/country_codes_regions.csv` and `dbt_in_123/seeds/geo_calling_codes.csv` (small, committed). **BREAKING** filename normalization: `geo-calling-codes_EN.csv` → `geo_calling_codes.csv` (snake-case, drops `_EN` suffix).
- **BREAKING** remove `dbt_in_123/models/example/` (the default `dbt init` scaffold).
- Ship `dbt_in_123/profiles.example.yml` using `path: "{{ env_var('OTB_DUCKDB_PATH', '../data/otb.duckdb') }}"`, with a commented-out MotherDuck `outputs:` block as the documented optional cloud path.
- Rewrite root `README.md`: travel-data domain, Excel-as-motivation framing, install steps for win/mac/linux, link to GH Release for the data file, MotherDuck optional callout.
- Update `openspec/project.md`: filename `otb.duckdb` (not `raw.duckdb`), domain (travel/On The Beach + airport reference), table list, seeds.
- Expand `main.py` to expose three subcommands callable as `python main.py <cmd>`:
  - `prep` — download `otb.duckdb` from the GH Release asset with checksum verification (idempotent).
  - `debug` — dispatch to `dbt debug` from `dbt_in_123/`.
  - `build` — dispatch to `dbt seed && dbt run && dbt test`.
- Add `duckdb` (python lib) and `httpx` to `pyproject.toml`; refresh `uv.lock`.
- `.gitignore`: exclude `data/otb.duckdb`, `data/raw/`, `dbt_packages/`, `target/`, `.DS_Store`, `logs/*.log`, `.opencode/`.
- Remove committed 0-byte placeholders `data/raw.duckdb` and `lessons/01_setup.md` (the lesson is authored fresh in change `add-lesson-01-setup`).

## Impact

- **Affected specs**: `workshop-foundations` (new capability).
- **Affected code**:
  - `data/` (placeholder removed; real DB gitignored)
  - `dbt_in_123/dbt_project.yml`
  - `dbt_in_123/profiles.example.yml` (new)
  - `dbt_in_123/models/sources.yml` (new)
  - `dbt_in_123/models/example/` (deleted)
  - `dbt_in_123/seeds/country_codes_regions.csv` (new)
  - `dbt_in_123/seeds/geo_calling_codes.csv` (new)
  - `sql/load_raw_airports.sql`, `sql/load_raw_prices.sql` (cleaned)
  - `scripts/build_otb_duckdb.py` (new)
  - `main.py`
  - `pyproject.toml`, `uv.lock`
  - `README.md`
  - `openspec/project.md`
  - `.gitignore`
  - `lessons/01_setup.md` (placeholder removed)
- **Dependent changes**: `add-lesson-01-setup`, `add-lesson-02a-cleaning`, `add-lesson-02b-joining`, `add-lesson-03-analytics` all depend on this change.
