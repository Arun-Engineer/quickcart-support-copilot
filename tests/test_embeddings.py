from app.embeddings import *

def test_dot_product_hand_example():

    a = [0.8, 0.6, 0]
    b = [0.96, 0.28, 0]

    dot_prod = round(dot_product(a, b),4)

    assert dot_prod == 0.936


def test_vector_length_three_four():

    a = [3, 4]

    vector = vector_length(a)

    assert vector == 5.0

def test_cosine_identical():

     a = [1, 2, 3]
     b = a

     cosine = cosine_similarity(a, b)

     assert cosine == 1.0

def test_cosine_unrelated():

    a = [1, 0]
    b = [0, 1]

    cosine = cosine_similarity(a, b)

    assert cosine == 0.0

def test_cosine_opposite():

    a = [1, 0]
    b = [-1, 0]

    cosine = cosine_similarity(a, b)

    assert cosine == -1.0

def test_cosine_zero_vector():

    a = [0, 0]
    b = [1, 1]

    cosine = cosine_similarity(a,b)

    assert cosine in (0.0, 'division by zero <- Due to this error.')