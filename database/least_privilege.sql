-- Run as a MySQL administrative account, not the application account.
CREATE USER IF NOT EXISTS 'promptwall_app'@'localhost'
IDENTIFIED BY 'STRONG_PASSWORD';

GRANT SELECT ON promptwall_db.* TO 'promptwall_app'@'localhost';

SHOW GRANTS FOR 'promptwall_app'@'localhost';

-- The application account intentionally receives no INSERT, UPDATE, DELETE,
-- DROP, ALTER, CREATE, or GRANT OPTION privileges.
