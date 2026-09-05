# PocketLedger

PocketLedger is a mobile-first financial identity platform for South Africa's informal economy, operating natively inside WhatsApp.

## Architecture

- **ingestion-gateway**: Node.js/Express service handling Twilio webhooks.
- **ledger-engine**: Python/FastAPI service for transaction logic, AI parsing, and Evidence Trust scoring.
- **smart-contracts**: Solidity contracts for anchoring state to Ethereum Sepolia.
- **dashboard**: Streamlit dashboard for lenders to view Financial Identity Passports.

## Running Locally

Use `docker-compose up` to start PostgreSQL, Redis, and RabbitMQ dependencies.

# PocketLedger
