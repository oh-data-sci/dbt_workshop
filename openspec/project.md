# project context

## purpose
this is a repo of materials for a workshop aimed to train sql-literate beginners in using dbt (data build tool). it is comprised of three expedited lessons expected to be given to trainees over a 2 hour in-person session.

the workshop is called **dbt in 1-2-3** and is structured as three progressive lessons:
1. **setup** — initialise a dbt project, connect to duckdb, understand project structure
2. **cleaning** — write dbt models that clean raw tables (consistent types, imputed nulls, date parsing); outputs a silver/cleaned schema
3. **analytics** — build analytical/aggregation models on top of the cleaned schema; outputs a data product layer

## tech stack
- **uv** — environment and package management
- **python ≥ 3.12** — scripting and automation
- **dbt-core ≥ 1.11.7** — transformation orchestration
- **dbt-duckdb ≥ 1.10.1** — duckdb adapter for dbt
- **duckdb (local)** — warehouse engine; database file `raw.duckdb` provided to participants
- **motherduck (optional)** — cloud duckdb, free tier, for participants who want a cloud target

## repository structure

```
dbt_workshop/                                 # workshop root folder
  ├── data/                                   # raw data files / source database file
  ├── dbt_in_123/                             # the dbt project folder
  │   ├── analyses/                           # optional sql calculations (no persistent output)
  │   ├── macros/                             # reusable jinja/sql macros
  │   ├── models/                             # dbt model definitions
  │   │   ├── <business_domain>/              # organise models by domain/source
  │   │   │   ├── 02a_clean_<table>.sql       # lesson 2a: cleaning transformations
  │   │   │   ├── 02b_join_<t1>_<t2>.sql     # lesson 2b: joining cleaned tables
  │   │   │   ├── 03_summary_<table>.sql      # lesson 3: analytical aggregations
  │   │   │   └── schema.yml                  # model documentation and tests
  │   │   └── sources.yml                     # raw layer source table declarations
  │   ├── seeds/                              # static reference data loaded by dbt
  │   ├── tests/                              # custom dbt test definitions
  │   ├── snapshots/                          # scd snapshots (if needed)
  │   ├── README.md
  │   └── dbt_project.yml                     # dbt project config (name: dbt_in_123, profile: dbt_in_123)
  ├── lessons/                                # participant instruction files (markdown)
  │   ├── 01_setup.md
  │   ├── 02a_cleaning.md
  │   ├── 02b_joining.md
  │   └── 03_data_products_semantics.md
  ├── logs/                                   # dbt run log captures
  ├── main.py                                 # master python script for running transformation stages
  ├── pyproject.toml                          # project packaging (uv)
  ├── README.md
  └── uv.lock
```

## project conventions

### model naming convention
models are prefixed with a two-part code indicating lesson stage and sub-step:
- `02a_` — lesson 2, cleaning step (one model per raw table)
- `02b_` — lesson 2, joining step (cleaned tables joined for analytics readiness)
- `03_` — lesson 3, analytical aggregations / data products

### materialization
- default materialization: **view**
- override per model in the model's `{{ config(...) }}` block if needed (e.g. `table` for expensive aggregations)

### code style
- prefer sql over python for dbt models
- prefer common table expressions over nested subqueries
- sql keywords in all caps
- table/field names in lower case
- new field names: descriptive and concise
- comments in lower case
- dates exclusively in iso-8601 format
- example:
```sql
  SELECT
    t1.column1            AS column_one,
    t2.column123          AS column_purpose,
    SUM(t1.value_column1) AS total            -- in <units>
  FROM
    table1 t1 LEFT JOIN table2 t2 ON t1.primary_key_col=t2.foreign_key_col
  WHERE
    t1.value_column2 > t2.comparative_value_column
  GROUP BY
    t1.column1,
    t2.column123
```

### architecture patterns
- use uv to manage the python environment; all participants install deps via `uv sync`
- provide `main.py` as a convenience script for running full transformation stages
- provide setup instructions for:
  - recent versions of windows
  - macos
  - common linux distributions (ubuntu/debian focus)
- assume participants arrive on workshop day with dbt installed and the dbt project cloned and configured

### testing strategy
- test each dbt model locally against the duckdb instance (`dbt test`)
- test-driven development for the python setup/automation scripts

### git workflow
- development work in feature branches
- merge to main via pull request

## domain context
- training assumes basic knowledge of sql, including window functions
- source data is a small "brighton-data" dataset provided as a duckdb file (`raw.duckdb`)
- the raw layer contains tables from two distinct sources (details tbd as data is prepared)
- raw tables are declared in `sources.yml` and referenced in models via `{{ source(...) }}`

## important constraints
- workshop duration: ~2 hours, in-person
- participants must have environment set up before the session begins
- models should be simple enough for beginners to understand and extend during the workshop
- avoid advanced dbt features (snapshots, exposures, metrics) unless they serve a clear teaching goal

## external dependencies
- duckdb database file (`raw.duckdb`) — to be prepared and distributed to participants ahead of workshop
- dbt profiles.yml — participants configure locally to point at their duckdb file path
