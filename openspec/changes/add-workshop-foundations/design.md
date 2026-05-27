# Design: add-workshop-foundations

## Context

The workshop is a 2-hour, in-person, beginner-targeted introduction to dbt against a local DuckDB. Participants are SQL-literate (including window functions) with basic CLI skills, little or no prior dbt experience, and a heavy Excel background — many will be encountering a real warehouse-style query engine for the first time.

The repo is currently scaffolded but non-functional: 0-byte placeholders, `dbt init` boilerplate, and uncommitted local edits in the main worktree that have diverged from `openspec/project.md`/`README.md`. The dataset chosen (On The Beach travel-pricing export + airport-codes reference; ~1 M + 85 K rows) is deliberately too large for Excel — that constraint motivates the whole workshop.

Foundations exists to bring the repo to a state where a clean clone + `uv sync && python main.py prep` + `dbt debug && dbt seed` works end-to-end, so subsequent lesson changes can focus on teaching content rather than infrastructure.

## Goals / Non-Goals

**Goals**
- A clean clone reaches a working `dbt debug` and `dbt seed` baseline in <60 seconds of human time, ~1–2 minutes wall-clock.
- Zero hardcoded user-specific paths in any committed artifact.
- Travel-data narrative is consistent across `README.md`, `openspec/project.md`, and any docs.
- Instructor's data-prep pipeline (CSV → DuckDB) is reproducible but isolated from the participant flow.
- MotherDuck cloud path is documented as a labelled, optional alternative — not required by the main flow.

**Non-Goals**
- Authoring lesson content (lessons 01–03 are separate change proposals).
- Loading the air-quality CSVs (`2021_2025_brighton_and_hove_*.csv`) — out of scope; the travel + airports dataset is sufficient for the workshop and keeps the narrative coherent.
- Supporting non-DuckDB warehouses (Postgres, Snowflake, etc.) in the participant profile template.
- Automating the GitHub Release asset upload — published manually by the instructor with `gh release create`.

## Decisions

### Decision: Host `otb.duckdb` on GitHub Releases

- **What**: Attach `otb.duckdb` (~42 MB) as a release asset on this repo at a versioned tag (e.g. `workshop-data-v1`). `main.py prep` downloads from the unauthenticated release URL.
- **Why**: Zero external infrastructure; versionable alongside the code; free; public-curl friendly; survives across instructors.
- **Alternatives considered**:
  - **AWS S3 / Cloudflare R2** — more "real cloud" feel but adds account/bucket maintenance overhead and an extra cost surface for a free workshop.
  - **Git LFS** — keeps the file "in" the repo but adds an LFS setup step for every participant and the LFS bandwidth quota is metered.
  - **Rebuild-from-CSVs every time** — most authentic ELT, but requires hosting ~280 MB of source CSVs and slows the first-run experience by ~30+ seconds.

### Decision: `main.py prep` is download-only

- **What**: The participant-facing prep step only downloads the prebuilt `otb.duckdb`. CSV ingestion lives in `scripts/build_otb_duckdb.py`, called only by the instructor when preparing a new release.
- **Why**: Determinism for participants; the workshop starts in seconds; the messy ~280 MB CSV ingest is isolated from the workshop flow; reduces what can go wrong on participant laptops during the session.

### Decision: Env-var path with relative default in `profiles.yml`

- **What**: `path: "{{ env_var('OTB_DUCKDB_PATH', '../data/otb.duckdb') }}"`. Default resolves relative to the `dbt_in_123/` working dir; overridable via `OTB_DUCKDB_PATH` env var.
- **Why**: Portable across machines and OSes; no `/Users/oskar/...` paths in the repo; participants get a working default with zero configuration; the env-var override is a single, documented knob for advanced cases (different on-disk location, MotherDuck token, etc.).
- **Alternatives considered**:
  - **Absolute path per participant** — what the current uncommitted draft does; high friction; mistakes likely.
  - **Pure relative path with no env-var override** — works but inflexible; breaks if a participant runs dbt from anywhere other than `dbt_in_123/`.

### Decision: Reference data shipped as `dbt seed`, not as `raw.*` tables

- **What**: `country_codes_regions.csv` and `geo_calling_codes.csv` (small, ~25 KB combined) ship as `dbt seed` files in `dbt_in_123/seeds/`, not as tables inside `data/otb.duckdb`'s `raw` schema.
- **Why**:
  - Gives lessons 02b/03 a natural, authentic reason to introduce `dbt seed` as a first-class concept.
  - Keeps the semantic boundary clean: `raw.*` = external source data; seeds = static repo-managed reference data.
  - Tiny files belong in git; large files (`otb.duckdb`) don't.
- **Trade-off**: seeds are loaded into the same target schema as models, not into `raw` — a participant might briefly wonder why airports comes from `source(...)` while country codes come from `ref(...)`. The lesson 01 + 02b docs will explain the distinction.

### Decision: Snake-case + drop `_EN` on seed filenames

- **What**: `geo-calling-codes_EN.csv` → `geo_calling_codes.csv`. Hyphens to underscores; locale suffix removed since no other locales are planned.
- **Why**: dbt derives the seed table name from the filename; snake-case keeps it `SELECT * FROM geo_calling_codes` (idiomatic SQL identifier) without quoting. The `_EN` suffix is dead weight in a single-locale workshop.

### Decision: Capability boundary `workshop-foundations`

- **What**: Single capability covering data warehouse, dbt project skeleton, sources, seeds, profile template, orchestration, root docs.
- **Why**: All of these are tightly coupled — none of them works without the others, none of them is independently meaningful as a unit. Splitting (e.g. `dbt-skeleton` vs `data-warehouse`) would force artificial dependencies between sub-capabilities authored at the same time. The lesson capabilities (`lesson-setup`, `cleaning-models`, etc.) are separate because they CAN stand alone as the content layers above the foundations.

## Risks / Trade-offs

- **GH Release URL drift** → if the release tag is renamed/deleted, `main.py prep` breaks. Mitigation: pin to a specific tag in `main.py`; commit a checksum so participants notice silent corruption; document the tag explicitly in README.
- **Travel-data domain may confuse readers expecting the brighton/ONS narrative from the original `README.md`** → Mitigation: rewrite `README.md` and `openspec/project.md` in this change; reference the dataset's source (the `onthebeachexport.csv` export) in the data description.
- **42 MB DB download could be slow on conference wifi** → Mitigation: pre-arrival instructions in `lessons/01_setup.md` (future change) tell participants to run `python main.py prep` before the session.
- **`COUNT(DISTINCT )` SQL syntax error in `sql/load_raw_airports.sql`** is a latent bug — fix is trivial but easy to forget. Verification step 7.6 implicitly catches it (build fails if the load script doesn't run cleanly).
- **MotherDuck path is documented but untested in CI** → Mitigation: out of scope for foundations; lesson 01 includes the snippet; participants who use it self-verify.

## Migration Plan

This is a greenfield foundations layer with no prior production state to migrate. The only state to handle is:

1. **Committed 0-byte placeholders** (`data/raw.duckdb`, `lessons/01_setup.md`) — removed via `git rm`; replaced (for `lessons/01_setup.md`) in a downstream change.
2. **Default `models/example/`** — removed via `git rm -r`; participants who already ran `dbt init` against this scaffold can `git pull` cleanly.
3. **Uncommitted local edits in the main worktree** (lessons/01_setup.md@757B, modified README.md, modified dbt_project.yml, sql/load_raw_*.sql, plan.md) — absorbed as starting points for the new artifacts; not committed as-is.

**Rollback**: `git revert` the foundations commit. The participant-facing `data/otb.duckdb` is gitignored, so revert doesn't delete it from disk; participants would need to re-run prep against the previous release tag.

## Open Questions

None blocking foundations. Curriculum-time questions (audience profile detail, lesson timings, tests coverage policy) are deferred to the per-lesson change proposals.
