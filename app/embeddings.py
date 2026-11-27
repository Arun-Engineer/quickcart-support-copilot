import math
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

EMDEDED_MODEL = "text-embedding-3-small"

def get_embedding(text):
    client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model = EMDEDED_MODEL, input = text)

    return response.data[0].embedding

def dot_product(a, b):

    product = []

    for i in range(len(a)):
        mulitply = a[i] * b[i]

        product.append(mulitply)

    return sum(product)

def vector_length(a):

    total = 0

    for i in range(len(a)):

        square = a[i] * a[i]

        total = total + square

    return math.sqrt(total)

def cosine_similarity(a, b):

    length_a = vector_length(a)
    length_b = vector_length(b)

    if length_a == 0 or length_b == 0:
        return 0.0

    product_of_lengths = length_a * length_b

    cos_sim = dot_product(a, b) / product_of_lengths

    return cos_sim