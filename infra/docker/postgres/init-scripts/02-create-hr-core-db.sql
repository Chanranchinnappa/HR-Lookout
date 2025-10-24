-- =============================================================================
-- POSTGRES INITIALIZATION SCRIPT
-- Create HR Core service database
-- =============================================================================

-- Create HR Core database (for Phase 2)
CREATE DATABASE hr_core_db WITH OWNER hr_admin;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE hr_core_db TO hr_admin;

-- Log success
SELECT 'HR Core database created successfully' AS status;
