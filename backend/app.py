from flask import Flask, jsonify, request

from database.gateway import DatabaseGateway
from AI.query_parser import GeminiQueryParser

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

    result = gateway.execute(user,query)

    status_code = 200 if result["decision"] == "ALLOW" else 403

    return jsonify(result), status_code


@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json()

    if not data:
        return jsonify({"decision": "BLOCK", "reason":"REQUEST_BODY_MISSING"}), 400


    user = data.get("user")
    message = data.get("message")

    if not user or not message:
        return jsonify({
            "decision": "BLOCK",
            "reason": "USER_OR_MESSAGE_MISSING"
        }), 400

    try:
        structured_query = llm.parse(message, user)
        result = gateway.execute(user, structured_query)

        response = {
            "natural_language_request": message,
            "structured_query": structured_query,
            **result
        }

        status_code = 200 if result["decision"] == "ALLOW" else 403
        return jsonify(response), status_code

    except Exception as exc:
        return jsonify({
            "decision": "BLOCK",
            "reason": "LLM_QUERY_PARSING_FAILED",
            "error": str(exc)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)