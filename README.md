# QuickCart Support Copilot

A FastAPI service that answers quick-commerce customer questions (orders, refunds, delivery, substitutions) using an LLM, and returns a structured JSON answer with a confidence score and a "needs human" flag for escalation.

Built by a QA engineer with 4+ years in quick-commerce. It is built test-first: the LLM is faked in unit tests, and CI runs on every push and pull request.

---

## What it does now

| Endpoint | Method | What it does |
| --- | --- | --- |
| `/health` | GET | Liveness check. Returns 200 if the service is up |
| `/chat` | POST | Takes a customer question and returns a structured answer from the LLM |

**Request** (`question` must be 1–500 characters, otherwise 422):

```json
{ "question": "My order is late, can I get a refund?" }
```

**Response (validated with Pydantic):**

```json
{
  "answer": "…",
  "confidence": 0.82,
  "needs_human": false
}
```

**Behaviour worth knowing:**

- Off-topic questions (not about QuickCart) are refused by the system prompt.
- If the LLM call fails (bad API key, network error), `/chat` returns 503 with a safe error message. It never returns a 200 with a broken answer.

---

## Tech stack

Python 3.14 · FastAPI · Pydantic · OpenAI API (JSON mode) · pytest + FastAPI TestClient · GitHub Actions

---

## Project structure

```text
app/
  main.py         FastAPI app: /health and /chat
  models.py       Pydantic models: ChatRequest, SupportAnswer
  llm_client.py   System prompt, LLM call, reply parsing, error handling
tests/
  test_models.py      Pydantic validation tests
  test_llm_client.py  Reply-parsing and error-result tests
  test_api.py         Endpoint tests with TestClient (LLM faked with monkeypatch)
.github/workflows/
  tests.yml       CI: runs pytest on every push and pull request
.env.example      Template for the required environment variables
```

---

## Run locally (Windows / PowerShell)

```powershell
git clone https://github.com/Arun-Engineer/quickcart-support-copilot.git
cd quickcart-support-copilot
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
copy .env.example .env        # then open .env and add your OpenAI API key
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to try the endpoints in the browser.

---

## Run tests

```powershell
python -m pytest -v
```

15 tests. No API key is needed: the LLM call is replaced with a fake using pytest's `monkeypatch`, so the tests are fast, free and give the same result every time.

---

## CI

Every push and every pull request to `main` triggers GitHub Actions (`.github/workflows/tests.yml`). It starts a fresh machine, installs Python 3.14 and the dependencies, and runs the full test suite. `main` is protected: changes only reach it through a pull request with a passing test check.

---

## Known issues

- **Angry-customer escalation:** the reply sometimes says "contact customer support" instead of setting `needs_human: true`.
- **Token cost:** the system prompt adds about 60 tokens to every call.
- **Invented facts:** delivery times and policy details can be made up, because the model has no access to real policy documents yet. RAG (below) fixes this.
- **Confidence score:** the LLM reports its own confidence, and that number isn't calibrated. Don't treat it as a real probability.

---

## Roadmap

- [ ] RAG over QuickCart policy/FAQ documents, with citations and an "I don't know" answer for out-of-scope questions
- [ ] Eval suite: golden Q&A set, recall@k, faithfulness and answer relevancy
- [ ] Prompt-injection and PII tests
- [ ] Eval-gated CI: block a merge if faithfulness drops below a threshold
