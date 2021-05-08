/*
 * ITAM-Data - Product Architecture - Master Liliana Millán
 * Project: Chicago Food Inspections - Team 05
 * Script: Create tables for clean and processed data...
 */

/* ================================= procesamiento task cleaning ================================= */
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
sin_mnth real,
cos_mnth real,
sin_wkd real,
cos_wkd real,
label_results int
);
COMMENT ON TABLE procdata.limpieza IS 'Almacena en RDS la BD limpia';

/* ================================= procesamiento task Feature Engineering ================================= */
DROP TABLE IF EXISTS procdata.feat_eng;
CREATE TABLE procdata.feat_eng (
label_risk int,
label_results int,
level varchar(8),
class text
);
COMMENT ON TABLE procdata.feat_eng IS 'Almacena en RDS la BD con las variables del FE';
