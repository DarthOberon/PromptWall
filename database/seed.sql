USE promptwall_db;

INSERT IGNORE INTO roles (role_id, role_name) VALUES
(1, 'Student'), (2, 'Faculty'), (3, 'Admin');

INSERT IGNORE INTO users (user_id, username, role_id) VALUES
(1, 'student_101', 1),
(2, 'student_102', 1),
(6, 'faculty_201', 2),
(7, 'faculty_202', 2),
(8, 'admin_001', 3);

INSERT IGNORE INTO students (student_id, user_id, name, department, semester) VALUES
(101, 1, 'Demo Student 101', 'Computer Science', 4),
(102, 2, 'Demo Student 102', 'Computer Science', 4),
(205, 3, 'Demo Student 205', 'Information Technology', 4);

INSERT IGNORE INTO faculty (faculty_id, user_id, name, department) VALUES
(201, 6, 'Demo Faculty 201', 'Computer Science'),
(202, 7, 'Demo Faculty 202', 'Information Technology');

INSERT IGNORE INTO courses (course_id, course_name, faculty_id) VALUES
(301, 'Database Systems', 201),
(302, 'Operating Systems', 201),
(401, 'Computer Networks', 202);

INSERT IGNORE INTO faculty_course_access (faculty_id, course_id) VALUES
(201, 301), (201, 302), (202, 401);

INSERT IGNORE INTO attendance (student_id, course_id, attendance_date, status) VALUES
(101, 301, '2026-08-01', 'Present'),
(101, 302, '2026-08-02', 'Present'),
(102, 301, '2026-08-01', 'Absent'),
(205, 401, '2026-08-01', 'Present');

INSERT IGNORE INTO marks (student_id, course_id, exam_type, marks) VALUES
(101, 301, 'Midterm', 82.00),
(101, 302, 'Midterm', 76.00),
(102, 301, 'Midterm', 68.00),
(205, 401, 'Midterm', 88.00);

INSERT IGNORE INTO security_policies (role_name, table_name, requires_row_restriction) VALUES
('Student', 'attendance', TRUE),
('Student', 'marks', TRUE),
('Student', 'students', TRUE),
('Faculty', 'attendance', TRUE),
('Faculty', 'marks', TRUE),
('Faculty', 'students', TRUE),
('Admin', 'attendance', FALSE),
('Admin', 'marks', FALSE),
('Admin', 'students', FALSE);
