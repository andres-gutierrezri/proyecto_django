-- -------------------
-- Base de Datos MySQL
-- -------------------

-- Consultas en la Base de Datos de MySQL

-- Consultar la versión de MySQL
SELECT VERSION() AS "Version MySQL";

-- Mostrar información sobre la conexión actual
STATUS;

-- Consultar la zona horaria
SELECT @@system_time_zone AS "Time Zone";

-- Consultar los plugins instalados
SHOW plugins;

-- Consultar las bases de datos
SHOW DATABASES;

-- Mostrar las tablas de la base de datos
-- USE `DB_NAME`;
-- SHOW tables;

-- Mostrar las tablas de todas las bases de datos
/*
SELECT TABLE_SCHEMA AS "Database", TABLE_NAME AS "Tables"
FROM information_schema.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_SCHEMA, TABLE_NAME;
*/
