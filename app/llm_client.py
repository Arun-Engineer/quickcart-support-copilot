# app/llm_client.py

import os
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, APIConnectionError

load_dotenv()

MODEL = "gpt-4o-mini"

# def ask_llm(question:str, temperature: float = 1) -> dict:
#     api_key = os.getenv("OPENAI_API_key")
#     if api_key is None:
#         raise ValueError("OPENAI_API_KEY is missing. Check your .env file.")

#     client = OpenAI(api_key= api_key)

#     response = client.chat.completions.create(
#         model = MODEL,
#         messages = [
#             {"role": "system", "content": "you are a support assistant for QUickCart, a quick-commerce grocery app. Answer in 2 sentences are less."},
#             {"role": "user", "content": question},
#         ],
#         temperature = temperature
#     )

#     answer = response.choices[0].message.content
#     tokens = response.usage.total_tokens

#     result = {"answer": answer, "tokens": tokens}
#     return result

# if __name__ == "__main__":
#     print(ask_llm("How long does delivery usually take?"))

def ask_llm(question: str, temperature: float = 0) -> dict:

    api_key = os.getenv("OPENAI_API_KEY")

    if api_key is None:
        raise ValueError("OPENAI_API_KEY is missing. Check your .env file.")

    client = OpenAI(api_key = api_key)

    try:
        response = client.chat.completions.create(
            model = MODEL,
            messages = [
                {"role": "system", "content": "Your a support assistant for QuickCart, a quick-commerce grocery app. Answer in 2 sentences or less."},
                {"role": "user", "content": question},
            ],
            temperature = temperature,
        )

    except AuthenticationError:
        return {"answer": None, "tokens": 0, "error": "Invalid API Key"}
    except APIConnectionError:
        return {"answer": None, "tokens": 0, "error": "Could not reach OPENAI. Check Internet."}

    answer = response.choices[0].message.content
    tokens = response.usage.total_tokens

    result = {"answer": answer, "tokens": tokens, "error": None}
    return result

if __name__ == "__main__":
    print(ask_llm("How long does delivery usually take?"))
