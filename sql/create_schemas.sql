/* ******* Schema Creation *******

 Script: Create schemas:
     > metadata to store info and processed data result of cleaning
     > select model
     > api and dashboard.
*/

DROP SCHEMA IF EXISTS metadata CASCADE;
CREATE SCHEMA metadata;

DROP SCHEMA IF EXISTS procdata CASCADE;
CREATE SCHEMA procdata;

DROP SCHEMA IF EXISTS api CASCADE;
CREATE SCHEMA api;

DROP SCHEMA IF EXISTS dsh CASCADE;
CREATE SCHEMA dsh;
