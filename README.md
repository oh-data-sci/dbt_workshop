dbt in 1-2-3
===
# introduction
this repo is a workshop giving an introduction to `dbt` (think: data build tool).

`dbt` is a python based management tool for data transformations in data warehouses. it orchestrates the 't' in 'etl', or 'elt'. the transformations are defined in `SQL` and `jinja`, and actually run on the data warehouse engine (typically in the cloud).

## preparation and prerequisites
to participate helpfully in this workshop, you will need a laptop with:
- a copy of this repo installed
- `uv` installed
- `duckdb` installed
- `dbt` installed (this means installing `dbt-core` and `dbt-duckdb`).
- brighton-data database file in duckdb format

# lessons 

## 1-setup
our first task will be to set up a dbt project on your machines.
- pull down this repository 
- inside the project folder run `dbt init`
- 

for this workshop, we will provide you with a `duckdb` database in the form of a file you can load onto your local machine. this database has a small number of tables from two sources. these tables constitute the `raw` layer (sometimes called bronze). think of them as data copied as-is from a data source in production.


## 2-cleaning
our second task will be to define a set to data cleaning transformations on the raw data and create a set of views that have consistent data types applied, where dates are interpreted as such, where missing values are imputed if intended value is obvious, and where relatable tables are joined to form a more useful data component for analytics. after showing you how to write and apply one such transformation, we will hand you a set of models to apply to the raw tables. the output is placed into a cleaned schema optimised for analytics (sometimes called the silver layer).

## 3-analytics
the next step is to develop the analytical data products based off the cleaned schema and develop that into the data product layer. for our purposes it will be landed in the same schema as the cleaned data.



## structure
project structure is work in progress. anticipated outcome is something akin to:

```
dbt_workshop/                                 # workshop root folder
  ├── data/                                   # (raw) data files, database file
  ├── dbt_in_123/                             # the dbt project folder
  │   ├── analyses/                           # optional sql script calcuations that don't create persistent results
  │   ├── macros/                             # optional definitions of calculations that get repeated
  │   ├── models/                             # definitions of the data transformations
  │   │   ├── business_function_one/          # top organisation level of transformations
  │   │   │   ├── 02a_clean_table1.sql        # a definition (sql code) of a table cleaning transformation
  │   │   │   ├── 02a_clean_table2.sql        # a definition of another table's cleaning transformation
  │   │   │   ├── 02a_clean_table3.sql
  │   │   │   ├── 02b_join_tab1_tab3.sql      # a definition of a new view, by joining two (cleaned) tables
  │   │   │   ├── 02b_join_tab2_tab3.sql      # another definition of a view, by joining two other tables
  │   │   │   ├── 02b_join_tab1_tab3.sql
  │   │   │   ├── 03_summary_tab1.sql         # a new data table definition, made from analytical computation of cleaned data
  │   │   │   ├── 03_summary_tab2.sql
  │   │   │   ├── 03_summary_tab3.sql
  │   │   │   └── schema.yml
  │   │   └── sources.yml                     # list of tables in raw table schema
  ├── lessons/                                # lesson instruction files
  │   ├── presentation.key                    # instructor's slides: intro to dbt, how-tos
  │   ├── 01_setup.md                         # dbt project setup, downloads
  │   ├── 02a_cleaning.md                     # first transformation on raw schema
  │   ├── 02b_joining.md                      # joining tables for preparation of analytical functions
  │   └── 03_data_products_semantics.md       # analytical calculations for use in dashboards
  ├── logs/                                   # dbt run log captures 
  │   └── dbt.log
  ├── main.py                                 # master python script for executing entire stages of transformation
  ├── pyproject.toml                          # project packaging information 
  ├── README.md                               # this file 
  │   ├── seeds/                              # instructions to get project started from fresh source data
  │   ├── tests/                              # definitions of test runs
  │   ├── README.md                           # dbt project description
  │   └── dbt_project.yml                     # root dbt project definition file (where to find source, models etc.)
  └── uv.lock                                 # code project library version lock
```
