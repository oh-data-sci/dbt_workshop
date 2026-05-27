## ADDED Requirements

### Requirement: Raw DuckDB Warehouse

The workshop SHALL provide a single-file DuckDB database at `data/otb.duckdb` containing a `raw` schema with two tables: `raw.airports` (airport metadata, approximately 85,000 rows) and `raw.prices` (On The Beach holiday-pricing export, approximately 1,085,000 rows). The database file SHALL NOT be committed to the git repository.

#### Scenario: Database available after prep

- **WHEN** a participant runs `python main.py prep` in a fresh clone
- **THEN** `data/otb.duckdb` exists on disk
- **AND** `duckdb data/otb.duckdb -c "SELECT COUNT(*) FROM raw.prices"` returns a row count greater than zero

#### Scenario: Database file is gitignored

- **WHEN** `git status` is run after a successful `python main.py prep`
- **THEN** `data/otb.duckdb` does not appear in the untracked or modified lists

### Requirement: Hosted Data Delivery

The prebuilt `otb.duckdb` SHALL be downloadable without authentication from a GitHub Release asset on this repository, and the download SHALL be verifiable against a known SHA-256 checksum recorded in the orchestration script.

#### Scenario: Public download succeeds

- **WHEN** `main.py prep` issues an HTTP GET to the recorded GitHub Release asset URL
- **THEN** the response is a 200 status with the database file body
- **AND** the SHA-256 of the body matches the checksum embedded in `main.py`

#### Scenario: Checksum mismatch aborts prep

- **WHEN** the downloaded body's SHA-256 does not match the recorded checksum
- **THEN** `main.py prep` exits with a non-zero status
- **AND** does not overwrite any existing `data/otb.duckdb`

### Requirement: dbt Project Skeleton

The `dbt_in_123/dbt_project.yml` file SHALL declare project name `dbt_in_123` and profile `dbt_in_123`, configure the path `models/otb/` as the active models directory with default materialization `view`, enable the `seeds/` path, and contain no references to the `example/` scaffold.

#### Scenario: dbt parses cleanly

- **WHEN** `dbt parse` runs from `dbt_in_123/` against a configured profile
- **THEN** the command exits with status zero
- **AND** no warning mentioning `example/` is emitted

#### Scenario: Models folder is otb

- **WHEN** `dbt list --resource-type model` runs after foundations is applied
- **THEN** no model under `models/example/` is listed

### Requirement: Source Declarations

A file `dbt_in_123/models/sources.yml` SHALL declare a source named `otb_raw` (schema `raw`) with two tables, `airports` and `prices`, each listing its columns with a name and a brief description.

#### Scenario: Sources visible to dbt

- **WHEN** `dbt list --resource-type source` runs from `dbt_in_123/`
- **THEN** the output includes `source.dbt_in_123.otb_raw.airports`
- **AND** the output includes `source.dbt_in_123.otb_raw.prices`

#### Scenario: Source columns are documented

- **WHEN** a reader opens `dbt_in_123/models/sources.yml`
- **THEN** each declared column on `airports` and `prices` has a non-empty `description` field

### Requirement: Static Reference Seeds

The `dbt_in_123/seeds/` directory SHALL contain two committed CSV files, `country_codes_regions.csv` and `geo_calling_codes.csv`, with snake_case filenames suitable as dbt-derived table names.

#### Scenario: Seeds load

- **WHEN** `dbt seed` runs from `dbt_in_123/`
- **THEN** both seeds materialize as tables in the default target schema
- **AND** each materialized seed contains at least one row

#### Scenario: Filenames are snake_case

- **WHEN** the seeds directory is listed
- **THEN** no filename contains a hyphen
- **AND** no filename contains an `_EN` locale suffix

### Requirement: Portable Profile Template

The repository SHALL ship a profile template at `dbt_in_123/profiles.example.yml` that resolves the DuckDB path via `env_var('OTB_DUCKDB_PATH', '../data/otb.duckdb')`, and SHALL include a commented-out MotherDuck `outputs:` block documenting the optional cloud target. The template SHALL NOT contain any hardcoded user-home or absolute paths.

#### Scenario: Default path works from dbt project dir

- **WHEN** a participant copies `profiles.example.yml` to `~/.dbt/profiles.yml` and runs `dbt debug` from `dbt_in_123/` without setting `OTB_DUCKDB_PATH`
- **THEN** the connection resolves to `../data/otb.duckdb` and `dbt debug` reports "All checks passed!"

#### Scenario: Env var override works

- **WHEN** a participant runs `OTB_DUCKDB_PATH=/tmp/x.duckdb dbt debug` with `/tmp/x.duckdb` a valid DuckDB file
- **THEN** the connection resolves to `/tmp/x.duckdb` and `dbt debug` reports "All checks passed!"

#### Scenario: No hardcoded user paths

- **WHEN** the profile template is grepped for `/Users/` or `C:\\Users\\`
- **THEN** no matches are found

### Requirement: Workshop Orchestration Script

A script `main.py` SHALL expose three subcommands callable as `python main.py <cmd>`: `prep` (download and verify `data/otb.duckdb`), `debug` (dispatch to `dbt debug` from `dbt_in_123/`), and `build` (dispatch to `dbt seed && dbt run && dbt test` from `dbt_in_123/`). The `prep` subcommand SHALL be idempotent.

#### Scenario: Prep is idempotent

- **WHEN** `python main.py prep` runs twice in succession from a clean clone
- **THEN** the first invocation downloads the file
- **AND** the second invocation is a no-op because the file is present and its checksum matches

#### Scenario: Build runs the full pipeline

- **WHEN** `python main.py build` runs after a successful `prep` and profile setup
- **THEN** `dbt seed`, `dbt run`, and `dbt test` are invoked in that order from `dbt_in_123/`
- **AND** all three steps exit with status zero

### Requirement: MotherDuck Optional Documentation

The root `README.md` SHALL describe a labelled "Optional: cloud target via MotherDuck" subsection containing a signup link, token-configuration instructions, and the alternative `profiles.yml` snippet. The MotherDuck path SHALL NOT be required by the participant's default workflow.

#### Scenario: Optional path documented in README

- **WHEN** a reader opens `README.md`
- **THEN** a section heading mentioning MotherDuck appears
- **AND** that section contains a signup URL, a token-config step, and a YAML profile snippet

### Requirement: Travel-Domain Documentation Alignment

The repository's primary documentation (`README.md` and `openspec/project.md`) SHALL describe the workshop's actual dataset (the On The Beach holiday-pricing export plus airport reference data) rather than the historic brighton-and-hove ONS air-quality framing, and SHALL reference the database file as `otb.duckdb`.

#### Scenario: README describes travel data

- **WHEN** `README.md` is read after foundations is applied
- **THEN** the data description references On The Beach holiday-pricing data and airport reference data
- **AND** the database filename `otb.duckdb` appears at least once

#### Scenario: project.md is aligned

- **WHEN** `openspec/project.md` is read after foundations is applied
- **THEN** no reference to `raw.duckdb` remains as the database filename
- **AND** the listed seeds include `country_codes_regions` and `geo_calling_codes`
