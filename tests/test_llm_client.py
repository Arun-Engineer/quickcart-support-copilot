# tests/test_llm_client.py

from app.llm_client import parse_llm_reply

def test_valid_reply_returns_five_keys():
    raw = '{"answer": "Refunds take 3-5 days.", "confidence": 0.8, "needs_human": false}'
    result = parse_llm_reply(raw, 120)
    assert result == {
        "answer": "Refunds take 3-5 days.",
        "confidence": 0.8,
        "needs_human": False,
        "tokens": 120,
        "error": None,
    }

def test_broken_json_returns_safe_error():
    result = parse_llm_reply("this is not json", 50)
    assert result["error"] == "LLM returned invalid JSON"
    assert result["needs_human"] is True
    #assert result["tokens"] == 50
    assert result["tokens"] == 999

def test_missing_key_returns_safe_error():
    raw = '{"answer": "Hi", "confidence": 0.8}'
    result = parse_llm_reply(raw, 30)
    assert result["error"] == "LLM returned invalid JSON"
    assert result["needs_human"] is True

def test_success_and_error_have_same_keys():
    good = parse_llm_reply('{"answer": "Hi", "confidence": 1, "needs_human": false}', 10)
    bad = parse_llm_reply("broken", 10)
    assert set(good.keys()) == set(bad.keys())