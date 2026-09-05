# PocketLedger Ledger & Evidence Engine

The Ledger and Evidence Engine is a Python FastAPI service that forms the core of the PocketLedger platform.

## Responsibilities
- Manages the PostgreSQL database using SQLAlchemy.
- Encrypts PII at rest and handles all core logic.
- Implements the **Evidence Trust Engine** to weight transaction reliability and compute Business Health Scores.
- Integrates with the **Whisper API** for transcribing voice notes (immediately discarding audio).
- Integrates with **Google Gemini** for strict JSON-schema LLM parsing and the Explainable AI Business Advisor.
- Computes state hashes and submits them to the Ethereum Sepolia smart contract.

## Running Locally

1. Setup virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

2. Setup database:
Copy `.env.example` to `.env`, ensure your PostgreSQL server is running.
```bash
alembic upgrade head
python seed.py
```

3. Run server:
```bash
uvicorn main:app --reload
```
