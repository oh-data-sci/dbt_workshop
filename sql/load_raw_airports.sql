-- Load airport reference data into raw schema
-- Run from the repo root: duckdb data/otb.duckdb < sql/load_raw_airports.sql

CREATE SCHEMA IF NOT EXISTS raw;

DROP TABLE IF EXISTS raw.airports;
CREATE TABLE raw.airports AS
    SELECT * FROM 'data/raw/airport-codes.csv';
