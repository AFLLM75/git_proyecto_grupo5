CREATE DATABASE wifi_db;
\connect wifi_db

CREATE USER grupo5_user WITH PASSWORD 'patata';

ALTER ROLE grupo5_user SET client_encoding TO 'utf8';
ALTER ROLE grupo5_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE grupo5_user SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE wifi_db TO grupo5_user;

ALTER DATABASE wifi_db OWNER TO grupo5_user;