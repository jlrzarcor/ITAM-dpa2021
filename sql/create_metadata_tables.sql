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
COMMENT ON TABLE metadata.ingestion IS 'Almacena metadata de los datos ingestados de la API Chicago Food Inspections';


/* ================================= metadata task almacenamiento ================================= */

DROP TABLE IF EXISTS metadata.almacenamiento;
CREATE TABLE metadata.almacenamiento (
  fecha date,
  param_exec json,
  usuario varchar(10),
  num_regs_almac int,
  ruta_S3 text
);
COMMENT ON TABLE metadata.almacenamiento IS 'Almacena metadata de raw data';


/* ================================= metadata task limpieza y procesamiento ================================= */

DROP TABLE IF EXISTS metadata.limpieza;
CREATE TABLE metadata.cleaning (
  exec_date date,
  exec_param json,
  executer varchar(10),
  source_path text,
  nrows_prev int,
  ncols_prev int,
  nrows_after int,
  ncols_after int,
  nulls int
);
COMMENT ON TABLE metadata.cleaning IS 'Almacena metadata de la bd limpia';



/* ================================= metadata task feature engineering ================================= */

DROP TABLE IF EXISTS metadata.feat_eng;
CREATE TABLE metadata.feat_eng (
  exec_date date,
  exec_param json,
  executer varchar(10),
  source_path text,
  nrows_ohe int,
  ncols_ohe int,
  best_score real,
  time_exec real,
  best_rf text
);
COMMENT ON TABLE metadata.feat_eng IS 'Almacena metadata de feature engineering';



/* ================================= metadata test tasks passed ================================= */

DROP TABLE IF EXISTS metadata.unittest;
CREATE TABLE metadata.unittest (
  test_meth varchar(17),
  test_stat varchar(17),
  test_msg varchar(23),
  exec_date date,
  exec_param json,
  executer varchar(10)
);
COMMENT ON TABLE metadata.unittest IS 'Almacena metadatos de los test que aprobaron pass:); flag + para los test en task de luigi';



/* ================================= metadata task training ================================= */

DROP TABLE IF EXISTS metadata.training;
CREATE TABLE metadata.training (
  exec_date date,
  exec_param json,
  executer varchar(10),
  num_regs_str int,
  nrows_train int,
  nrows_test int,
  S3_path text
);
COMMENT ON TABLE metadata.training IS 'Almacena metadata de la bd limpia';


/* ================================= metadata task model ================================= */
 
DROP TABLE IF EXISTS metadata.modelo;
CREATE TABLE metadata.modelo (
  exec_date date,
  exec_param json,
  executer varchar(10),
  best_tree text,
  exec_time real,
  test_models text,
  score text,
  rank text
);
COMMENT ON TABLE metadata.modelo IS 'Almacena metadata del modelo';
