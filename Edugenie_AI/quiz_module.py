import json
import re
from typing import Any

from gemini_client import generate_text


def clean_json_block(text: str) -> str:
    """
    Removes Markdown code fences and extracts JSON
    from the model response.
    """

    text = text.strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        return text[start:end + 1]

    start = text.find("[")
    end = text.rfind("]")

    if start != -1 and end != -1:
        return text[start:end + 1]

    return text


def validate_quiz(data: Any) -> list:

    if isinstance(data, dict):
        questions = data.get("questions")

    elif isinstance(data, list):
        questions = data

    else:
        raise ValueError(
            "Invalid quiz format."
        )

    if not isinstance(questions, list):
        raise ValueError(
            "Quiz questions must be a list."
        )

    if len(questions) != 3:
        raise ValueError(
            "Quiz must contain exactly 3 questions."
        )

    validated = []

    for index, question in enumerate(questions, start=1):

        if not isinstance(question, dict):
            raise ValueError(
                f"Question {index} is invalid."
            )

        question_text = question.get("question")
        options = question.get("options")
        answer = question.get("answer")

        if not question_text:
            raise ValueError(
                f"Question {index} has no question text."
            )

        if not isinstance(options, list):
            raise ValueError(
                f"Question {index} options must be a list."
            )

        if len(options) != 4:
            raise ValueError(
                f"Question {index} must have exactly 4 options."
            )

        if not answer:
            raise ValueError(
                f"Question {index} has no correct answer."
            )

        if answer not in options:
            raise ValueError(
                f"Question {index} answer must match one option."
            )

        validated.append(
            {
                "question": str(question_text),
                "options": [
                    str(option)
                    for option in options
                ],
                "answer": str(answer),
            }
        )

    return validated


def generate_quiz(text: str) -> list:

    if not text.strip():
        raise ValueError("Text cannot be empty.")

    prompt = f"""
Create a multiple-choice quiz from the following educational content.

Content:
{text}

Return ONLY valid JSON.

The JSON must have exactly this structure:

{{
  "questions": [
    {{
      "question": "Question text",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "answer": "Correct option"
    }}
  ]
}}

Rules:
- Generate exactly 3 questions.
- Every question must have exactly 4 options.
- There must be exactly one correct answer.
- The answer must exactly match one of the options.
- Questions must be based only on the supplied content.
- Do not include explanations outside the JSON.
"""

    raw_response = generate_text(
        prompt,
        temperature=0.2,
        max_output_tokens=2000
    )

    cleaned = clean_json_block(raw_response)

    try:
        data = json.loads(cleaned)

    except json.JSONDecodeError as e:
        raise ValueError(
            f"Could not parse quiz JSON: {e}"
        )

    return validate_quiz(data)