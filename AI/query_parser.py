"""Gemini Based Natural-Language query parser for PromptWall """
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

SYSTEM_PROMPT = """
You are a query parser for PromptWall, an AI database security guardrail.

Your job is ONLY to convert a user's natural-language database request into 
a structured query JSON query.

Never generate SQL.

Return ONLY JSON with this structure:

{ 
    "operation": "SELECT",
    "table": "attendance",
    "columns": ["attendance_date", "status"],
    row_conditions":{}
}

Supported tables:
    - attendance
    - marks
    - students
    - courses

Only SELECT operations are allowed.

For attendacne:
allowed columns: attendance_date, status, course_id

For marks:
allowed columns: course_id, exam_type, marks 

For students:
allowed columns: student_id, name, department, semester

For courses:
allowed columns: course_id, course_name, faculty_id

If the user asks for "my" data, use the user's identity infromaition
porvided sepeately by the application.

Do not invent database fields.
Do not bypass access control.
Do not make authorization decisions.

"""

class GeminiQueryParser:
    def __init__(self):
        self.client = genai.Client()

    def parse(self, user_request: str, user: dict) -> dict:
        prompt = f"""
{SYSTEM_PROMPT}

Authenticated application user:
{json.dumps(user)}

User request:
{user_request}
"""
        response = self.client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            ),
        )

        return json.loads(response.text)

