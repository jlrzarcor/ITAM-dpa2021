/*
 * ITAM-Data - Product Architecture - Master Liliana Millán
 * Project: Chicago Food Inspections - Team 05
 * Script: Create tables for api data...
 */

/* ================================= procesamiento task api data ================================= */
DROP TABLE IF EXISTS api.scores;
CREATE TABLE api.scores (
    ingest_date date,
    index int, 
    aka_name varchar(90),
    license varchar(20),
    score real,
    prediction int
);
COMMENT ON TABLE api.scores IS 'Almacenar las predicciones de S3 RDS para API';


/* ================================= procesamiento dashboard data ================================= */
DROP TABLE IF EXISTS api.dash;
CREATE TABLE api.dash (
    ingest_date date,
    index int,
    aka_name varchar(90),
    license varchar(20),
    score real,
    prediction int
);
COMMENT ON TABLE api.dash IS 'Almacenar las predicciones de S3 RDS para dashboard';
