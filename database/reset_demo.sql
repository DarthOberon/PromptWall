
-- reset_demo.sql
-- Preserves: roles, users, audit_logs, security_policies.
-- Connect to promptwall_db before sourcing this file.
-- Do not use mysql --force.

DELIMITER //

DROP PROCEDURE IF EXISTS reset_promptwall_demo_data//

CREATE PROCEDURE reset_promptwall_demo_data()
BEGIN
    DECLARE roles_before BIGINT;
    DECLARE users_before BIGINT;
    DECLARE audit_before BIGINT;
    DECLARE policies_before BIGINT;

    -- Any SQL exception rolls back the deletion transaction.
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    -- Guard 1: correct database.
    IF COALESCE(DATABASE(), '') <> 'promptwall_db' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Reset aborted: select promptwall_db first.';
    END IF;

    -- Guard 2: explicit confirmation in this connection.
    IF COALESCE(@promptwall_reset_confirmed, 0) <> 1 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Reset aborted: explicit confirmation required.';
    END IF;

    -- Snapshot protected tables.
    SELECT COUNT(*) INTO roles_before FROM roles;
    SELECT COUNT(*) INTO users_before FROM users;
    SELECT COUNT(*) INTO audit_before FROM audit_logs;
    SELECT COUNT(*) INTO policies_before FROM security_policies;

    START TRANSACTION;

    -- Delete child rows first.
    DELETE FROM attendance;
    DELETE FROM marks;
    DELETE FROM student_course;
    DELETE FROM faculty_course_access;

    -- Then delete academic parent rows.
    DELETE FROM courses;
    DELETE FROM students;
    DELETE FROM faculty;

    -- Sanity check protected table counts before committing.
    IF (SELECT COUNT(*) FROM roles) <> roles_before
       OR (SELECT COUNT(*) FROM users) <> users_before
       OR (SELECT COUNT(*) FROM audit_logs) <> audit_before
       OR (SELECT COUNT(*) FROM security_policies) <> policies_before THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Reset aborted: protected table counts changed.';
    END IF;

    COMMIT;
END//

DELIMITER ;

CALL reset_promptwall_demo_data();

DROP PROCEDURE reset_promptwall_demo_data;
