-- Database initialization script for Todo API
-- This script runs when the MySQL container starts for the first time

-- Create the database if it doesn't exist (will be created by MYSQL_DATABASE env var)
-- CREATE DATABASE IF NOT EXISTS todo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use the database (will be set by MYSQL_DATABASE env var)
-- USE todo_db;

-- Create a user for the application (will be created by MYSQL_USER env var)
-- CREATE USER IF NOT EXISTS 'todo_user'@'%' IDENTIFIED BY 'todo_password';

-- Grant privileges to the user (will be done by MYSQL_USER env var)
-- GRANT ALL PRIVILEGES ON todo_db.* TO 'todo_user'@'%';

-- Flush privileges to ensure they take effect
FLUSH PRIVILEGES;

-- Show databases to confirm
SHOW DATABASES;
