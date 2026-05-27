-- Load On The Beach holiday-pricing export into raw schema
-- Run from the repo root: duckdb data/otb.duckdb < sql/load_raw_prices.sql

CREATE SCHEMA IF NOT EXISTS raw;

DROP TABLE IF EXISTS raw.prices;
CREATE TABLE raw.prices AS
    SELECT * FROM 'data/raw/onthebeachexport.csv';
