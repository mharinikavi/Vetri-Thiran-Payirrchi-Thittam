from gemini_client import generate_text


def answer_question(question: str) -> str:

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    prompt = f"""
You are EduGenie, an educational AI assistant.

Answer the student's question clearly and accurately.

Question:
{question}

Instructions:
- Use simple language.
- Explain difficult terms when necessary.
- Give examples when useful.
- Do not unnecessarily make the answer very long.
- Structure the answer with headings or bullet points when helpful.
"""

    return generate_text(
        prompt,
        temperature=0.3,
        max_output_tokens=1500
    )