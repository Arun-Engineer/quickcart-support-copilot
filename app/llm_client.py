# app/llm_client.py

import os
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, APIConnectionError
from pydantic import ValidationError
from app.models import SupportAnswer

load_dotenv()

MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You are a support assistant for QuickCart, a quick-commerce grocery app.
You ONLY help with QuickCart Topics: orders, delivery, payments, refunds, and account issues.
If the question is about anything else, politely say you can only help with QuickCart questions,
set "confidence" to 1 and "needs_human to false.
Reply ONLY with a JSON object with exactly these keys:
- "answer": your reply to the customer, 2 sentences or less
- "confidence": a number from 0 to 1, how sure you are that the answer is correct
- "needs_human": true if a human agent should take over (angry customer, refund dispute, safety issue, or you are unsure), otherwise false
"""

def parse_llm_reply(raw_text: str, tokens: int) -> dict:
    try:
        parsed = SupportAnswer.model_validate_json(raw_text)
    except ValidationError:
        result = error_result("LLM returned invalid JSON")
        result["tokens"] = tokens
        return result
        
    result = parsed.model_dump()
    result["tokens"] = tokens
    result["error"] = None
    return result

def error_result(message: str) -> dict:
    return {"answer": None, "confidence": 0, "needs_human": True, "tokens": 0, "error": message}

def ask_llm(question: str, temperature: float = 0) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key is None:
        raise ValueError("OPENAI_API_KEY is missing. Check your.env file.")

    client = OpenAI(api_key = api_key)

    try:
        response = client.chat.completions.create(
            model = MODEL,
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ],
            temperature = temperature,
            response_format = {"type": "json_object"},
        )

    except AuthenticationError:
        return error_result("Invalid API key")
    except APIConnectionError:
        return error_result("Could not reach OpenAI. Check internet.")

    raw_text = response.choices[0].message.content
    tokens = response.usage.total_tokens

    return parse_llm_reply(raw_text, tokens)

    

if __name__ == "__main__":

    questions = [
        "How long does delivery usuallay take?",
        "My order was wrong and I want a refund NOW, this is the third time!.",
        "What is the capital of France?.",
    ]

    for question in questions:
        print("Q: ", question)
        print(ask_llm(question))
        print()