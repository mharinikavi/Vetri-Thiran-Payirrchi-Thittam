import os

from gemini_client import generate_text


def explain_with_gemini(topic: str) -> str:

    prompt = f"""
You are an expert teacher.

Explain the following topic to a beginner:

Topic:
{topic}

Requirements:
- Use very simple language.
- Start with a short definition.
- Explain the important points.
- Give a simple real-world example.
- Use bullet points where useful.
- Make the explanation easy for a student to understand.
"""

    return generate_text(
        prompt,
        temperature=0.4,
        max_output_tokens=1800
    )


def explain_with_local_model(topic: str) -> str:

    try:
        from transformers import pipeline

    except ImportError:
        raise RuntimeError(
            "Local explanation mode requires transformers. "
            "Run: pip install -r requirements-local.txt"
        )

    model_name = os.getenv(
        "LOCAL_EXPLANATION_MODEL",
        "MBZUAI/LaMini-Flan-T5-783M"
    )

    generator = pipeline(
        "text2text-generation",
        model=model_name
    )

    prompt = f"""
Explain this topic simply for a beginner:

{topic}

Give:
1. Definition
2. Main points
3. Simple example
"""

    result = generator(
        prompt,
        max_new_tokens=300,
        do_sample=False
    )

    return result[0]["generated_text"].strip()


def explain_topic(topic: str) -> str:

    if not topic.strip():
        raise ValueError("Topic cannot be empty.")

    provider = os.getenv(
        "EXPLANATION_PROVIDER",
        "gemini"
    ).lower()

    if provider == "local":
        return explain_with_local_model(topic)

    return explain_with_gemini(topic)