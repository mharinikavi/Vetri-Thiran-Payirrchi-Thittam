import json

from quiz_module import clean_json_block, validate_quiz


def test_clean_json_block():

    raw = """```json
    {
        "questions": []
    }
    ```"""

    cleaned = clean_json_block(raw)

    data = json.loads(cleaned)

    assert "questions" in data


def test_validate_quiz():

    quiz = [
        {
            "question": "What is Python?",
            "options": [
                "Language",
                "Database",
                "Browser",
                "Operating System"
            ],
            "answer": "Language"
        },
        {
            "question": "What is FastAPI?",
            "options": [
                "Framework",
                "Database",
                "Game",
                "Compiler"
            ],
            "answer": "Framework"
        },
        {
            "question": "What is Gemini?",
            "options": [
                "AI model",
                "Keyboard",
                "Browser",
                "Operating System"
            ],
            "answer": "AI model"
        }
    ]

    result = validate_quiz(quiz)

    assert len(result) == 3
    assert all(
        len(question["options"]) == 4
        for question in result
    )