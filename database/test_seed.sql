
USE promptwall_test_db;

INSERT IGNORE INTO roles (role_id, role_name) VALUES
(1, 'Student'),
(2, 'Faculty'),
(3, 'Admin');

INSERT IGNORE INTO users (user_id, username, role_id) VALUES
(1, 'student_101', 1),
(2, 'student_102', 1),
(3, 'student_103', 1),
(4, 'student_104', 1),
(5, 'student_105', 1),
(6, 'faculty_201', 2),
(7, 'faculty_202', 2),
(8, 'admin_001', 3),
(9, 'student_106', 1),
(10, 'student_107', 1),
(11, 'student_108', 1),
(12, 'student_109', 1),
(13, 'student_110', 1),
(14, 'faculty_203', 2),
(15, 'faculty_204', 2),
(16, 'admin_002', 3);

INSERT IGNORE INTO students (student_id, user_id, name, department, semester) VALUES
(101, 1, 'Aarav Mehta', 'Computer Science', 5),
(102, 2, 'Diya Patel', 'Computer Science', 5),
(103, 3, 'Kabir Shah', 'Information Technology', 5),
(104, 4, 'Ananya Desai', 'Computer Science', 5),
(105, 5, 'Rohan Trivedi', 'Information Technology', 5),
(106, 9, 'Ishita Joshi', 'Computer Science', 5),
(107, 10, 'Dev Malhotra', 'Information Technology', 5),
(108, 11, 'Mira Vyas', 'Computer Science', 5),
(109, 12, 'Arjun Rao', 'Information Technology', 5),
(110, 13, 'Sara Nair', 'Computer Science', 5);

INSERT IGNORE INTO faculty (faculty_id, user_id, name, department) VALUES
(201, 6, 'Nisha Mehta', 'Computer Science'),
(202, 7, 'Rahul Desai', 'Information Technology'),
(203, 14, 'Priya Shah', 'Computer Science'),
(204, 15, 'Kunal Patel', 'Information Technology');

INSERT IGNORE INTO courses (course_id, course_name, faculty_id) VALUES
(301, 'Database Systems', 201),
(302, 'Operating Systems', 201),
(303, 'Computer Networks', 202),
(304, 'Software Engineering', 203),
(305, 'Web Technologies', 204),
(306, 'Cybersecurity Fundamentals', 203);

INSERT IGNORE INTO student_course (student_id, course_id) VALUES
(101, 301), (101, 302), (101, 304),
(102, 301), (102, 303), (102, 305),
(103, 301), (103, 303), (103, 306),
(104, 301), (104, 302), (104, 304),
(105, 302), (105, 303), (105, 305),
(106, 301), (106, 304), (106, 306),
(107, 302), (107, 305),
(108, 301), (108, 304),
(109, 303), (109, 306),
(110, 301), (110, 305);


INSERT IGNORE INTO faculty_course_access (faculty_id, course_id) VALUES
(201, 301),
(201, 302),
(202, 303),
(203, 304),
(204, 305),
(203, 306);

INSERT IGNORE INTO attendance (student_id, course_id, attendance_date, status) VALUES
(101, 301, '2026-08-01', 'Present'),
(101, 302, '2026-08-02', 'Present'),
(101, 304, '2026-08-03', 'Absent'),
(102, 301, '2026-08-01', 'Absent'),
(102, 303, '2026-08-02', 'Present'),
(102, 305, '2026-08-03', 'Present'),
(103, 301, '2026-08-01', 'Present'),
(103, 303, '2026-08-02', 'Absent'),
(103, 306, '2026-08-03', 'Present'),
(104, 301, '2026-08-01', 'Present'),
(104, 302, '2026-08-02', 'Absent'),
(104, 304, '2026-08-03', 'Present'),
(105, 302, '2026-08-01', 'Present'),
(105, 303, '2026-08-02', 'Present'),
(105, 305, '2026-08-03', 'Absent'),
(106, 301, '2026-08-01', 'Present'),
(106, 304, '2026-08-02', 'Present'),
(106, 306, '2026-08-03', 'Absent'),
(107, 302, '2026-08-01', 'Present'),
(107, 305, '2026-08-02', 'Absent'),
(108, 301, '2026-08-01', 'Present'),
(108, 304, '2026-08-02', 'Present'),
(109, 303, '2026-08-01', 'Absent'),
(109, 306, '2026-08-02', 'Present'),
(110, 301, '2026-08-01', 'Present'),
(110, 305, '2026-08-02', 'Present');

INSERT IGNORE INTO marks (student_id, course_id, exam_type, marks) VALUES
(101, 301, 'Midterm', 82.00),
(101, 302, 'Midterm', 76.00),
(101, 304, 'Midterm', 89.00),
(102, 301, 'Midterm', 68.00),
(102, 303, 'Midterm', 74.00),
(102, 305, 'Midterm', 91.00),
(103, 301, 'Midterm', 85.00),
(103, 303, 'Midterm', 63.00),
(103, 306, 'Midterm', 78.00),
(104, 301, 'Midterm', 92.00),
(104, 302, 'Midterm', 81.00),
(104, 304, 'Midterm', 87.00),
(105, 302, 'Midterm', 73.00),
(105, 303, 'Midterm', 88.00),
(105, 305, 'Midterm', 69.00),
(106, 301, 'Midterm', 79.00),
(106, 304, 'Midterm', 95.00),
(106, 306, 'Midterm', 72.00),
(107, 302, 'Midterm', 84.00),
(107, 305, 'Midterm', 71.00),
(108, 301, 'Midterm', 90.00),
(108, 304, 'Midterm', 86.00),
(109, 303, 'Midterm', 67.00),
(109, 306, 'Midterm', 82.00),
(110, 301, 'Midterm', 77.00),
(110, 305, 'Midterm', 93.00);


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
