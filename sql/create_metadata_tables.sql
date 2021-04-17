/*
 * ITAM-Data - Product Architecture - Master Liliana Millán
 * Project: Chicago Food Inspections - Team 05
 * Script: Create tables for metadata...
 */



/* ================================= metadata task ingestion ================================= */

DROP TABLE IF EXIST metadata.ingestion;
CREATE TABLE metadata.ingestion (
  fecha date,
  param_exec json,
  usuario varchar(10),
  num_regs_ing int
);
COMMENT ON TABLE metadata.ingestion IS 'Almacena metadata de los datos ingestados';
