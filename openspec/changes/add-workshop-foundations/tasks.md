# Tasks: add-workshop-foundations

## 1. Repo hygiene

- [x] 1.1 Remove `dbt_in_123/models/example/` (sql files and `schema.yml`).
- [x] 1.2 Remove committed 0-byte placeholder `data/raw.duckdb` from git.
- [x] 1.3 Remove committed 0-byte placeholder `lessons/01_setup.md` from git (the real lesson is authored in `add-lesson-01-setup`).
- [x] 1.4 Update `.gitignore` to exclude `data/otb.duckdb`, `data/raw/`, `dbt_packages/`, `target/`, `.DS_Store`, `logs/*.log`, `.opencode/`.

## 2. Data prep (instructor-only)

- [x] 2.1 Fix `sql/load_raw_airports.sql`: drop the broken `COUNT(DISTINCT )` line; isolate the `CREATE TABLE` step from exploration queries.
- [x] 2.2 Tidy `sql/load_raw_prices.sql`: isolate `CREATE TABLE` from exploration queries.
- [x] 2.3 Add `scripts/build_otb_duckdb.py` — ingests the two raw CSVs into `data/otb.duckdb` via duckdb-python; runs the cleaned `sql/load_raw_*.sql` scripts; idempotent (drops + recreates the `raw` schema).
- [ ] 2.4 Publish `data/otb.duckdb` as a GitHub Release asset (tag `workshop-data-v1`); record the URL and SHA-256 checksum in `main.py` and `README.md`. **NOTE: URL stubbed as TODO in main.py; to be completed by instructor after publishing the release.**

## 3. dbt project

- [x] 3.1 Rewrite `dbt_in_123/dbt_project.yml`: project key `dbt_in_123`, profile `dbt_in_123`, `models/otb/` with `+materialized: view`, seeds path enabled.
- [x] 3.2 Create `dbt_in_123/models/sources.yml` declaring source `otb_raw` with tables `airports` and `prices` and their column names + brief descriptions.
- [x] 3.3 Copy `data/raw/country_codes_regions.csv` → `dbt_in_123/seeds/country_codes_regions.csv`.
- [x] 3.4 Copy and rename `data/raw/geo-calling-codes_EN.csv` → `dbt_in_123/seeds/geo_calling_codes.csv` (snake-case, drops `_EN`).
- [x] 3.5 Ship `dbt_in_123/profiles.example.yml` with env-var path (`OTB_DUCKDB_PATH` default `../data/otb.duckdb`) plus a commented MotherDuck `outputs:` block.

## 4. Orchestration script

- [x] 4.1 Implement `main.py prep`: download from GH Release URL, verify SHA-256, place at `data/otb.duckdb`; no-op if file present and checksum matches.
- [x] 4.2 Implement `main.py debug`: chdir to `dbt_in_123/` and exec `dbt debug`.
- [x] 4.3 Implement `main.py build`: chdir to `dbt_in_123/` and exec `dbt seed && dbt run && dbt test`.
- [x] 4.4 Add `duckdb` and `httpx` to `pyproject.toml`; run `uv lock` to refresh `uv.lock`.

## 5. Docs

- [x] 5.1 Rewrite root `README.md`: travel-data domain narrative, Excel-as-motivation framing, install steps for windows/macos/linux, GH Release asset link, MotherDuck "Optional cloud target" callout.
- [x] 5.2 Update `openspec/project.md`: change `raw.duckdb` references to `otb.duckdb`, replace ONS/brighton-air-quality domain text with travel/airport+prices description, add `country_codes_regions` and `geo_calling_codes` as seeds.

## 6. OpenSpec

- [ ] 6.1 Confirm `openspec validate add-workshop-foundations --strict` exits 0.
- [ ] 6.2 (Post-deployment) archive via `openspec archive add-workshop-foundations`.

## 7. Verification

- [ ] 7.1 From a fresh clone: `uv sync && python main.py prep` produces `data/otb.duckdb`.
- [ ] 7.2 `cp dbt_in_123/profiles.example.yml ~/.dbt/profiles.yml && cd dbt_in_123 && dbt debug` → "All checks passed!".
- [ ] 7.3 `dbt list --resource-type source` lists `source.dbt_in_123.otb_raw.airports` and `source.dbt_in_123.otb_raw.prices`.
- [ ] 7.4 `dbt seed` materializes both seeds with row counts > 0.
- [ ] 7.5 `dbt parse` exits 0 with no warnings about `example/`.
- [ ] 7.6 `duckdb ../data/otb.duckdb -c "SELECT COUNT(*) FROM raw.prices"` returns ~1,085,919.
- [ ] 7.7 `python main.py prep` invoked a second time is a no-op (idempotency).
