from AI.query_parser import GeminiQueryParser

parser =  GeminiQueryParser()

user = {
    "user_id":1,
    "role":"Student",
    "student_id":101,
}

result = parser.parse("Show me my attendance", user)

print(result)