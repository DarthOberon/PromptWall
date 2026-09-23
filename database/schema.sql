-- PromptWall demo schema
CREATE DATABASE IF NOT EXISTS promptwall_db;
USE promptwall_db;

CREATE TABLE IF NOT EXISTS roles (
    role_id INT PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL UNIQUE,
    role_id INT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

CREATE TABLE IF NOT EXISTS students (
    student_id INT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    name VARCHAR(120) NOT NULL,
    department VARCHAR(100) NOT NULL,
    semester TINYINT NOT NULL CHECK (semester BETWEEN 1 AND 8),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS faculty (
    faculty_id INT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    name VARCHAR(120) NOT NULL,
    department VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(120) NOT NULL,
    faculty_id INT NOT NULL,
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
);

CREATE TABLE IF NOT EXISTS faculty_course_access (
    faculty_id INT NOT NULL,
    course_id INT NOT NULL,
    PRIMARY KEY (faculty_id, course_id),
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    attendance_date DATE NOT NULL,
    status ENUM('Present', 'Absent') NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    INDEX idx_attendance_student (student_id),
    INDEX idx_attendance_course (course_id)
);

CREATE TABLE IF NOT EXISTS marks (
    mark_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    exam_type VARCHAR(50) NOT NULL,
    marks DECIMAL(5,2) NOT NULL CHECK (marks BETWEEN 0 AND 100),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    INDEX idx_marks_student (student_id),
    INDEX idx_marks_course (course_id)
);

CREATE TABLE IF NOT EXISTS audit_logs (
    log_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NULL,
    decision VARCHAR(20) NOT NULL,
    reason VARCHAR(80) NOT NULL,
    table_name VARCHAR(100) NULL,
    operation VARCHAR(20) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS security_policies (
    policy_id INT PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR(50) NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    requires_row_restriction BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE KEY uq_role_table (role_name, table_name)
);
