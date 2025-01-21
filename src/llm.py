import os

import google.generativeai as genai
from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])


gemini_generation_config = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

gemini_model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=gemini_generation_config,
)


def process_gemini_response(response):
    """
    Extract text and token counts from Gemini API response
    Returns tuple of (text, dict with token counts)
    """
    # Extract text from the response
    text = response.candidates[0].content.parts[0].text

    # Extract token counts
    token_counts = {
        'prompt_tokens': response.usage_metadata.prompt_token_count,
        'completion_tokens': response.usage_metadata.candidates_token_count,
        'total_tokens': response.usage_metadata.total_token_count
    }

    return text, token_counts


async def get_gemini_response(prompt):
    """
    Get response from Gemini API for a given prompt
    """
    response = await gemini_model.generate_content_async(
        prompt,
    )

    text, token_count = process_gemini_response(response)

    return text
