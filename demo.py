"""Standalone console demonstration of the Access Control module."""

from pprint import pprint

from security.authorization import authorize_query
from temporary.test_users import TEST_USERS
from temporary.test_queries import (
    SAFE_ATTENDANCE_QUERY,
    OTHER_STUDENT_ATTENDANCE,
    UNAUTHORIZED_TABLE,
    UNAUTHORIZED_COLUMN,
    DROP_QUERY,
    FACULTY_ALLOWED,
    FACULTY_OUTSIDE_COURSE,
)


CASES = [
    ("Student 101 -> own attendance", TEST_USERS["student_101"], SAFE_ATTENDANCE_QUERY),
    ("Student 101 -> student 205 attendance", TEST_USERS["student_101"], OTHER_STUDENT_ATTENDANCE),
    ("Student -> unauthorized table", TEST_USERS["student_101"], UNAUTHORIZED_TABLE),
    ("Student -> unauthorized column", TEST_USERS["student_101"], UNAUTHORIZED_COLUMN),
    ("Student -> DROP TABLE", TEST_USERS["student_101"], DROP_QUERY),
    ("Faculty -> permitted course", TEST_USERS["faculty_201"], FACULTY_ALLOWED),
    ("Faculty -> outside course", TEST_USERS["faculty_201"], FACULTY_OUTSIDE_COURSE),
]


if __name__ == "__main__":
    for title, user, query in CASES:
        print(f"\n{title}")
        pprint(authorize_query(user, query))
