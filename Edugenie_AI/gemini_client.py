import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)


_client = None


def get_client():
    global _client

    if _client is not None:
        return _client

    if not API_KEY:
        raise RuntimeError(
            "Gemini API key not found. "
            "Please set GEMINI_API_KEY in your .env file."
        )

    _client = genai.Client(api_key=API_KEY)

    return _client


def generate_text(
    prompt: str,
    temperature: float = 0.3,
    max_output_tokens: int = 2048
) -> str:

    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    client = get_client()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        ),
    )

    text = getattr(response, "text", None)

    if not text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()