DROP DATABASE IF EXISTS my_user_database CASCADE;
CREATE DATABASE IF NOT EXISTS my_user_database;
USE my_user_database;
CREATE TABLE users (
    id uuid PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
    email STRING,
    full_name STRING,
    allergies STRING[],
    dietaryRestrictions STRING[],
    username STRING,
    UNIQUE INDEX users_name (username ASC)
);


