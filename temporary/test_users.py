"""Temporary development identities; not an authentication system."""

TEST_USERS = {
    "student_101": {
        "user_id": 1,
        "student_id": 101,
        "role": "Student",
    },
    "student_102": {
        "user_id": 2,
        "student_id": 102,
        "role": "Student",
    },
    "faculty_201": {
        "user_id": 6,
        "faculty_id": 201,
        "role": "Faculty",
        "permitted_course_ids": [301, 302],
    },
    "faculty_202": {
        "user_id": 7,
        "faculty_id": 202,
        "role": "Faculty",
        "permitted_course_ids": [401],
    },
    "admin_001": {
        "user_id": 8,
        "role": "Admin",
    },
}
