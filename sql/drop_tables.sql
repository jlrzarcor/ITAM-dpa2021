/*
 * ITAM-Data - Product Architecture - Master Liliana Millán
 * Project: Chicago Food Inspections - Team 05
 * Script: Drop single tables...
 */

DROP TABLE IF EXISTS metadata.ingestion;
DROP TABLE IF EXISTS metadata.almacenamiento;
DROP TABLE IF EXISTS metadata.cleaning;
DROP TABLE IF EXISTS metadata.feat_eng;
DROP TABLE IF EXISTS metadata.unittest;
DROP TABLE IF EXISTS metadata.training;
DROP TABLE IF EXISTS metadata.modelo;
DROP TABLE IF EXISTS metadata.biasfair;
DROP TABLE IF EXISTS metadata.predictions;

DROP TABLE IF EXISTS procdata.limpieza;
DROP TABLE IF EXISTS procdata.feat_eng;

DROP TABLE IF EXISTS api.scores;
DROP TABLE IF EXISTS dsh.model;

DROP TABLE IF EXISTS table_updates;
