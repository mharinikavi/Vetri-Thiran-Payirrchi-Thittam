from gemini_client import generate_text


def summarize_text(text: str) -> str:

    if not text.strip():
        raise ValueError("Text cannot be empty.")

    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following text in simple language.

Text:
{text}

Requirements:
- Keep the important information.
- Remove unnecessary repetition.
- Use simple student-friendly language.
- Use bullet points if they improve readability.
- Do not add information that is not present in the original text.
"""

    return generate_text(
        prompt,
        temperature=0.2,
        max_output_tokens=1200
    )