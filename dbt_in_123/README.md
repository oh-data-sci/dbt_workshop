dbt in 1-2-3
===

# introduction
this is a basic `dbt` project to demonstrate how to get started using dbt, to go along with the `dbt_workshop`, see [here:](https://github.com/oh-data-sci/dbt_workshop)

# get started
- set up your profile:
```
vi ~/.dbt/profiles.yml
```
- example profile content:
```yml
dbt_in_123:
  outputs:
    dev:
      type: duckdb
      path: full-path-to-dev-duckdb-database-file
      threads: 2

    prod:
      type: duckdb
      path: full-path-to-production-duckdb-database-file
      threads: 4

  target: dev
```

- check connection details:
```bash
dbt debug
```
- perform all transformations
```bash
dbt run
```
- run tests
```bash
dbt test
```

# resources:
- learn about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- check out [discourse](https://discourse.getdbt.com/) for a faq
- join the [chat](https://community.getdbt.com/) on slack for live discussions and support
- find [dbt events](https://events.getdbt.com) near you
- check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
