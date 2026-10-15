from flask import Flask, jsonify, request

from database.gateway import DatabaseGateway
from AI.query_parser import GeminiQueryParser
from security.request_safety import check_request_safety


app = Flask(__name__)

gateway = DatabaseGateway()
llm = GeminiQueryParser()

@app.route("/")
def home():
    return "PromptWall is runnig!"

@app.route("/api/query",methods=["POST"])
def query():
    data = request.get_json()

    if not data:
        return jsonify({"decision" : "BLOCK", "reason" : "REQUEST_BODY_MISSING"}), 400

    user = data.get("user")
    query_data = data.get("query")

    if not user or not query_data:
        return jsonify({"decision" : "BLOCK", "reason" : "USER_OR_QUERY_MISSING"}),400

    result = gateway.execute(user,query_data)

    status_code = 200 if result["decision"] == "ALLOW" else 403

    return jsonify(result), status_code



@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "decision": "BLOCK",
            "reason": "REQUEST_BODY_MISSING"
        }), 400

    user = data.get("user")
    message = data.get("message")

    if not isinstance(user, dict) or not user or not isinstance(message, str) or not message.strip():
        return jsonify({
            "decision": "BLOCK",
            "reason": "USER_OR_MESSAGE_MISSING"
        }), 400

    safe_to_parse, safety_reason = check_request_safety(message)

    if not safe_to_parse:
        return jsonify({
            "decision": "BLOCK",
            "reason": safety_reason,
            "natural_language_request": message,
            "structured_query": None
        }), 403

    try:
        parsed = llm.parse(message, user)
        app.logger.info(
            "DEBUG message=%r | parsed_conditions=%r",
            message,
            (parsed.get("query") or {}).get("row_conditions")
    if isinstance(parsed, dict) else None,
)
        app.logger.info("Debug: Parsed query: %s", parsed)

        if not isinstance(parsed, dict) or parsed.get("status") != "READY":
            reason = (
                parsed.get("reason", "UNSUPPORTED_OR_UNSAFE_REQUEST")
                if isinstance(parsed, dict)
                else "INVALID_MODEL_RESPONSE"
            )

            return jsonify({
                "decision": "BLOCK",
                "reason": reason,
                "natural_language_request": message,
                "structured_query": None
            }), 403

        structured_query = parsed.get("query")

        if not isinstance(structured_query, dict):
            return jsonify({
                "decision": "BLOCK",
                "reason": "INVALID_MODEL_RESPONSE",
                "structured_query": None
            }), 403

         # Students may only request their own marks and attendance.
        # A named-student request must never be silently treated as "self".
        if (
            user.get("role") == "Student"
            and structured_query.get("table") in {"marks", "attendance"}
            and structured_query.get("subject") != "self"
        ):
            return jsonify({
                "decision": "BLOCK",
                "reason": "CROSS_STUDENT_ACCESS_DENIED",
                "structured_query": None
            }), 403

        

        
        
        if user.get("role") == "Student":
            table = structured_query.get("table")
            conditions = structured_query.get("row_conditions")

            if not isinstance(conditions, dict):
                conditions = {}

            if table in {"attendance", "marks"}:
                student_id = user.get("student_id")

                if student_id is None:
                    return jsonify({
                        "decision": "BLOCK",
                        "reason": "ROW_ACCESS_DENIED",
                        "structured_query": None
                    }), 403

                # Require an explicit identity condition.
                # Do not silently substitute the logged-in student's ID.
                if "student_id" not in conditions:
                    return jsonify({
                        "decision": "BLOCK",
                        "reason": "ROW_RESTRICTION_MISSING",
                        "structured_query": None
                    }), 403

                # Reject queries targeting another student.
                if conditions["student_id"] != student_id:
                    return jsonify({
                        "decision": "BLOCK",
                        "reason": "ROW_ACCESS_DENIED",
                        "structured_query": None
                    }), 403

                structured_query["row_conditions"] = conditions


        if structured_query.get("operation") != "SELECT":
            return jsonify({
                "decision": "BLOCK",
                "reason": "OPERATION_NOT_ALLOWED",
                "structured_query": None
            }), 403

        result = gateway.execute(user, structured_query)

        return jsonify({
            "natural_language_request": message,
            "structured_query": structured_query,
            **result
        }), 200 if result.get("decision") == "ALLOW" else 403

    except Exception:
        app.logger.exception("PromptWall request failed")
        return jsonify({
            "decision": "BLOCK",
            "reason": "REQUEST_PROCESSING_FAILED",
            "structured_query": None
        }), 500



if __name__ == "__main__":
    app.run(debug=True)