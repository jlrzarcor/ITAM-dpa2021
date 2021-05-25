/* ******* Schema Creation *******

 Script: Create 2 schemas, metadata to store info and processed data result of cleaning, selecting and modeling.
*/

DROP SCHEMA IF EXISTS metadata CASCADE;
CREATE SCHEMA metadata;

DROP SCHEMA IF EXISTS procdata CASCADE;
CREATE SCHEMA procdata;

DROP SCHEMA IF EXISTS api CASCADE;
CREATE SCHEMA api;
