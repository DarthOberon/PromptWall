
from getpass import getpass
from backend.app import app

client = app.test_client()
password = getpass("Demo password: ")

login = client.post(
    "/api/login",
    json={"username": "student_101", "password": password},
)
print("Login:", login.status_code)

tests = [
    ("Own marks", "show me my marks"),
    ("Other student's marks", "show me arjun rao's marks"),
    ("Own attendance", "show me my attendance"),
]

for label, message in tests:
    response = client.post("/api/ask", json={"message": message})
    result = response.get_json() or {}
    print(
        f"{label}: status={response.status_code}, "
        f"decision={result.get('decision')}, "
        f"reason={result.get('reason')}"
    )
