/*
 * ITAM-Data - Product Architecture - Master Liliana Millán
 * Project: Chicago Food Inspections - Team 05
 * Script: Create tables for metadata...
 */



/* ================================= metadata task ingestion ================================= */

DROP TABLE IF EXISTS metadata.ingestion;
CREATE TABLE metadata.ingestion (
  fecha date,
  param_exec json,
  usuario varchar(10),
  num_regs_ing int
);
COMMENT ON TABLE metadata.ingestion IS 'Almacena metadata de los datos ingestados';


/* ================================= metadata cleaning ================================= */

DROP TABLE IF EXISTS metadata.cleaning;
CREATE TABLE metadata.cleaning (
  num_registros_antes_limpieza int
  num_registros_despues_limpieza int
  valores_nulos int
  tamano_df_limpio int
  fecha_ejecucion date
  executer varchar(10)
);
COMMENT ON TABLE metadata.cleaning IS 'Almacena metadata de los datos ingestados';


/* ================================= metadata feature engineering ================================= */

DROP TABLE IF EXISTS metadata.fe;
CREATE TABLE metadata.fe (
  best_score float64
  fi_out json
  time_exec float64
  df_shape varchar(10)
);
COMMENT ON TABLE metadata.fe IS 'Almacena metadata de los datos ingestados';


/* ================================= metadata almacenamiento ================================= */

DROP TABLE IF EXISTS metadata.almacenamiento;
CREATE TABLE metadata.almacenamiento (
  
);
COMMENT ON TABLE metadata.almacenamiento IS 'Almacena metadata de los datos ingestados';
