-- =============================================================================
-- POSTGRES INITIALIZATION SCRIPT
-- Create Keycloak database and user
-- =============================================================================

-- Create Keycloak user
CREATE USER keycloak_user WITH PASSWORD 'keycloak_db_password_2025';

-- Create Keycloak database
CREATE DATABASE keycloak WITH OWNER keycloak_user;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak_user;

-- Switch to keycloak database
\c keycloak

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO keycloak_user;

-- Log success
SELECT 'Keycloak database and user created successfully' AS status;
