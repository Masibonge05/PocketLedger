# PocketLedger Financial Identity Passport Dashboard

The Passport Dashboard is a lender-facing Streamlit application designed for live demos and production insights.

## Responsibilities
- Renders the pseudonymized business profile for lenders.
- Displays Operating history, total transactions, cumulative revenue, and revenue consistency.
- Visualizes the **PocketLedger Health Score** and **Evidence Confidence Level**.
- Provides a "Verify Integrity" action that compares live data against the Ethereum Sepolia blockchain hash.
- Gated behind mutual authentication and OAuth 2.0 consent scoping.

## Running Locally

1. Setup virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

2. Configure environment:
Copy `.env.example` to `.env` and set the `LEDGER_ENGINE_URL`.

3. Run dashboard:
```bash
streamlit run app.py
```
