/*
 * ITAM-Data - Product Architecture - Master Liliana Millán
 * Project: Chicago Food Inspections - Team 05
 * Script: Create tables for clean and processed data...
 */



/* ================================= metadata task cleaning ================================= */
DROP TABLE IF EXISTS procdata.limpieza;
CREATE TABLE procdata.limpieza (
aka_name varchar(90),
license varchar(20),
facility_type varchar(60),
label_risk int,
zip varchar(10),
inspection_date date,
inspection_type varchar(60),
violations_count int,
label_results int,
sin_mnth real,
cos_mnth real,
sin_wkd real,
cos_wkd real
);
COMMENT ON TABLE procdata.limpieza IS 'Almacena en RDS la BD limpia';
