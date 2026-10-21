
"""Authentication helpers for PromptWall."""

from database.connection import get_connection
from werkzeug.security import check_password_hash


def authenticate_user(username: str, password: str):
    """Return database-derived account identity, or None."""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                users.user_id,
                users.username,
                users.password_hash,
                roles.role_name
            FROM users
            JOIN roles ON users.role_id = roles.role_id
            WHERE users.username = %s
            LIMIT 1
            """,
            (username,),
        )
        account = cursor.fetchone()

        if not account or not account.get("password_hash"):
            return None

        if not check_password_hash(account["password_hash"], password):
            return None

        user = {
            "user_id": account["user_id"],
            "username": account["username"],
            "role": account["role_name"],
        }

        if account["role_name"] == "Student":
            cursor.execute(
                "SELECT student_id FROM students WHERE user_id = %s LIMIT 1",
                (account["user_id"],),
            )
            student = cursor.fetchone()

            if not student:
                return None

            user["student_id"] = student["student_id"]

        elif account["role_name"] == "Faculty":
            cursor.execute(
                "SELECT faculty_id FROM faculty WHERE user_id = %s LIMIT 1",
                (account["user_id"],),
            )
            faculty = cursor.fetchone()

            if not faculty:
                return None

            faculty_id = faculty["faculty_id"]

            cursor.execute(
                """
                SELECT course_id
                FROM faculty_course_access
                WHERE faculty_id = %s
                """,
                (faculty_id,),
            )
            permitted_courses = cursor.fetchall()

            user["faculty_id"] = faculty_id
            user["permitted_course_ids"] = [
                row["course_id"] for row in permitted_courses
            ]

        elif account["role_name"] != "Admin":
            return None

        return user

    finally:
        cursor.close()
        connection.close()
