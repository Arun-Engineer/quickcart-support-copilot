# tests/test_api.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ------------------------FAKE LLM FUNCTIONS (NO INTERNET, NO COST)--------------------------------
def fake_ask_llm_success(question: str, temperature: float = 0) -> dict:
    return {"answer": "Fake answer", "confidence": 0.9, "needs_human": False, "tokens": 10, "error": None}


def fake_ask_llm_down(question:str, temperature: float = 0,) -> dict:
    return {"answer": None, "confidence": 0, "needs_human": True, "tokens": 0,
            "error": "Could not reach OpenAI. Check Internet."}


#----------------------T1: Health -------------------
def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

#-----------------------T2: valid chat (LLM faked)------------------
def test_chat_valid_question_returns_200(monkeypatch):
    monkeypatch.setattr("app.main.ask_llm", fake_ask_llm_success)
    response = client.post("/chat", json = {"question": "where is my order?"})
    assert response.status_code == 200
    assert response.json()["answer"] == "Fake answer"

#-----------------------T3, T6, T7: bad bodies -> 422--------------------
def test_chat_missing_question_returns_422():
    response = client.post("/chat", json ={})
    assert response.status_code == 422

def test_chat_number_question_returns_422():
    response = client.post("/chat", json = {"question": 12345})
    assert response.status_code == 422

def test_chat_empty_question_returns_422():
    response = client.post("/chat", json = {"question": ""})
    assert response.status_code == 422


#------------------------T4: Wrong method----------------------------
def test_chat_get_returns_405():
    response = client.get("/chat")
    assert response.status_code == 405

#------------------------T5: Unknown Route---------------------------
def test_unknown_route_returns_404():
    response = client.get("/orders")
    assert response.status_code == 404

#------------------------T8: OpenAI down -> 503(LLM faked)---------------------
def test_chat_llm_down_returns_503(monkeypatch):
    monkeypatch.setattr("app.main.ask_llm", fake_ask_llm_down)
    response = client.post("/chat", json = {"question": "where is my order?"})
    assert response.status_code == 503
    assert response.json()["detail"]["needs_human"] is True