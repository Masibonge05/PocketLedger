# PocketLedger

**PocketLedger** is a mobile-first financial identity platform for South Africa's informal economy, operating natively inside WhatsApp. The system lets unbanked and underbanked merchants (spaza shops, kota vendors, salons, mobile mechanics) log sales, manage inventory, and issue receipts via voice note or text in English and isiZulu, with zero new apps to install.

Every logged action is weighted for reliability by an **Evidence Trust Engine**, compiled into a Business Health Score, and periodically anchored to the Ethereum Sepolia blockchain as a tamper-proof hash. The output is a portable Financial Identity Passport that a merchant can consent-share with lenders, insurers, and suppliers to unlock credit.

## Tech Stack
- **Ingestion layer:** Node.js with Express (Twilio/Meta WhatsApp Business API)
- **Ledger & Evidence Engine:** Python with FastAPI
- **Database:** PostgreSQL (SQLAlchemy)
- **Queue & Rate Limiting:** Celery with RabbitMQ, Redis
- **AI/ML:** Whisper API (Voice), Google Gemini (Parsing & Advisor)
- **Blockchain:** Solidity (Ethereum Sepolia), Web3.py
- **Dashboard:** Streamlit

## Architecture

```text
[ WhatsApp / Merchant ]
          │ (TLS 1.3 + Twilio HMAC Signature)
          ▼
[ Ingestion Gateway (Node.js/Express) ] ── (ephemeral storage: audio dropped post-transcription)
          │ (mutual TLS / internal network)
          ▼
[ Core Ledger & Evidence Engine (Python/FastAPI) ] ── (AES-256 encrypted Postgres)
          │
          ├──► [ Whisper API ] (voice → text)
          ├──► [ Google Gemini API ] (text → structured transaction JSON)
          │
          └──► [ State Hash Generator (SHA-256) ]
                         │ (one-way hash of merchant_id + health_score + cumulative_revenue)
                         ▼
          [ PocketLedgerAnchor.sol on Ethereum Sepolia ]
                         │
                         ▼
          [ Passport Dashboard (Streamlit) ] (lender-facing, consent-gated)
```

## Running Locally

1. **Prerequisites**: Docker, Docker Compose
2. Run `docker-compose up` to start PostgreSQL, Redis, and RabbitMQ dependencies.
3. Setup environment variables for each service (see `.env.example` in each directory).
4. Run each service (see individual READMEs for details).
