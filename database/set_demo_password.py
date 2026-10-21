
"""Set demo passwords for PromptWall test accounts."""
import os
import getpass

import mysql.connector
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv(override=True)

if os.getenv("DB_NAME") != "promptwall_test_db":
    raise RuntimeError(
        "Safety check failed: DB_NAME must be promptwall_test_db"
    )

def main():
    password = getpass.getpass("Enter a demo password for all 16 accounts: ")
    confirm = getpass.getpass("Confirm demo password: ")

    if len(password) < 12:
        print("Use a password with at least 12 characters.")
        return

    if password != confirm:
        print("Passwords do not match.")
        return

    password_hash = generate_password_hash(password)

    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "promptwall_test_db"),
        user=os.getenv("DB_USER", "promptwall_app"),
        password=os.getenv("DB_PASSWORD", ""),
    )

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE users
            SET password_hash = %s
            WHERE user_id BETWEEN 1 AND 16
            """,
            (password_hash,),
        )
        connection.commit()
        print(f"Updated password hashes for {cursor.rowcount} accounts.")
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()
