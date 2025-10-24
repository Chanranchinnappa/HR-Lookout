-- =============================================================================
-- POSTGRES INITIALIZATION SCRIPT
-- Create Payroll service database
-- =============================================================================

-- Create Payroll database (for Phase 5)
CREATE DATABASE payroll_db WITH OWNER hr_admin;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE payroll_db TO hr_admin;

-- Log success
SELECT 'Payroll database created successfully' AS status;

