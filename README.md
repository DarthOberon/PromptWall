# PromptWall – Access Control & Database Engineer

Standalone college-project implementation of the **Access Control & Database Engineer** portion of PromptWall – AI Database Security Guardrail.

## Scope

This module works independently and does **not** require Gemini/OpenAI, a chatbot, prompt-injection detection, jailbreak detection, risk scoring, Streamlit, Plotly, an audit dashboard, group integration, or cloud deployment.

## Architecture

```text
Temporary Test User
        |
        v
Temporary Query Object
        |
        v
Authorization Engine
   +----+----+----+
   |    |    |    |
  RBAC Column  Row-Level
   |    |    |  Security
   +----+----+----+
        |
   ALLOW / BLOCK
        |
        v
Database Gateway
        |
   Parameterized SQL
        |
        v
      MySQL
```

## Responsibilities implemented

- MySQL connection using `.env`
- Relational database schema and demo seed data
- Least-privilege MySQL application user
- RBAC for Student, Faculty, and Admin
- Table-level access
- Column-level allowlists
- Row-Level Security
- Central fail-closed authorization
- Temporary development identities
- Structured temporary query objects
- Parameterized SELECT gateway
- Pytest security tests

## Database design

The demo schema contains:

- `roles`
- `users`
- `students`
- `faculty`
- `courses`
- `faculty_course_access`
- `attendance`
- `marks`
- `audit_logs`
- `security_policies`

The data is fictional and intended only for demonstration.

## Security model

### RBAC

Only `Student`, `Faculty`, and `Admin` are recognized roles. The role is read from the user context, not from the query.

The current MVP is read-only at the application layer. `SELECT` is the only permitted operation.

### Column permissions

Column access uses explicit allowlists. A role receives access only to columns declared for that role/table.

### Row-Level Security

- Student: must include a `student_id` condition matching the authenticated user's `student_id`.
- Faculty: must include a `course_id` condition belonging to the faculty member's permitted course set.
- Admin: follows the broader admin policy.
- Missing required row restrictions fail closed.

The authorization layer never treats a user-supplied student ID as proof of identity.

### Least privilege

The application account should have only `SELECT` permission. See `database/least_privilege.sql`.

Do not use MySQL `root` for application queries.

### Gateway

The gateway accepts structured query dictionaries rather than arbitrary SQL. It authorizes first, then builds a parameterized `SELECT` statement. Values are bound with `%s` placeholders.

## Installation

Python 3.10+ is recommended.

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configure `.env`

Copy `.env.example` to `.env` and set your local MySQL credentials.

Never commit `.env`.

## Initialize MySQL

Run `database/schema.sql` using an administrative MySQL account.

Then run `database/seed.sql`.

Create the restricted application account with `database/least_privilege.sql`, replacing `STRONG_PASSWORD` with a strong local password.

Example:

```sql
CREATE USER 'promptwall_app'@'localhost'
IDENTIFIED BY 'STRONG_PASSWORD';

GRANT SELECT ON promptwall_db.* TO 'promptwall_app'@'localhost';

SHOW GRANTS FOR 'promptwall_app'@'localhost';
```

The application account should not receive `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `CREATE`, or `GRANT OPTION` privileges.

## Run the standalone demonstration

From the project root:

```bash
python demo.py
```

Expected decisions include:

```text
Student 101 -> own attendance
{'decision': 'ALLOW', 'reason': 'AUTHORIZED'}

Student 101 -> student 205 attendance
{'decision': 'BLOCK', 'reason': 'ROW_ACCESS_DENIED'}

Student -> unauthorized table
{'decision': 'BLOCK', 'reason': 'TABLE_ACCESS_DENIED'}

Student -> unauthorized column
{'decision': 'BLOCK', 'reason': 'COLUMN_ACCESS_DENIED'}

Student -> DROP TABLE
{'decision': 'BLOCK', 'reason': 'OPERATION_NOT_ALLOWED'}

Faculty -> permitted course
{'decision': 'ALLOW', 'reason': 'AUTHORIZED'}

Faculty -> outside course
{'decision': 'BLOCK', 'reason': 'ROW_ACCESS_DENIED'}
```

## Run tests

```bash
pytest -q
```

The authorization/RBAC/RLS/gateway tests do not require a live MySQL server. They validate the security logic and parameterized query construction.

For a real database connection, configure `.env` and call `database.connection.test_connection()` or run an application integration test against your local MySQL instance.

## Current limitations

- Authentication is represented by temporary development identities only.
- No AI/LLM integration is included.
- The gateway intentionally supports only structured `SELECT` requests in this MVP.
- MySQL must be installed separately for live database execution.
- Faculty row restrictions are modeled using temporary permitted course IDs.
- This project does not claim 100% security.

## Security principles demonstrated

- Least privilege
- Fail closed
- Allowlist permissions
- Parameterized SQL
- No hardcoded secrets
- No root application account
- Do not trust user-provided role
- Do not trust user-provided student ID as authorization proof
- Authorize before database execution
- Block unauthorized operations before they reach MySQL

## Standalone scope statement

This is the temporary standalone **Access Control & Database Engineer** implementation for PromptWall. It is intentionally independent of unfinished team modules and can be demonstrated without any AI/LLM component.
