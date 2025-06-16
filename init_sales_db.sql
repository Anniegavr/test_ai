-- Create the separate sales database and table
CREATE DATABASE sales_db;
\connect sales_db;

CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    product TEXT NOT NULL,
    sale_date DATE NOT NULL,
    amount NUMERIC(10,2) NOT NULL
);
