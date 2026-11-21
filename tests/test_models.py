# tests/test_models.py

import pytest
from pydantic import ValidationError
from app.models import SupportAnswer

def test_valid_answer_is_accepted():
    answer = SupportAnswer(answer = "Hi", confidence = 0.5, needs_human = False)
    assert answer.confidence == 0.5

def test_confidence_above_1_is_rejected():
    with pytest.raises(ValidationError):
        SupportAnswer(answer = "Hi", confidence = 1.5, needs_human = False)

def test_missing_needs_human_is_rejected():
    with pytest.raises(ValidationError):
        SupportAnswer(answer= "Hi", confidence = 0.5)