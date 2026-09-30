from gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:

    if not topic.strip():
        raise ValueError("Topic cannot be empty.")

    prompt = f"""
You are EduGenie, a personalized learning assistant.

Create a structured learning path for:

Topic:
{topic}

Organize the learning path into:

1. Beginner Level
2. Intermediate Level
3. Advanced Level

For every level include:
- Concepts to learn
- Suggested practice
- Small project or activity
- Useful resource types

Also provide:
- Recommended learning order
- Prerequisites
- Final project idea

Keep everything beginner-friendly and practical.
"""

    return generate_text(
        prompt,
        temperature=0.4,
        max_output_tokens=2500
    )