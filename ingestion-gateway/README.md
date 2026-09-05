# PocketLedger Ingestion Gateway

The Ingestion Gateway is a Node.js/Express service that serves as the entry point for merchants interacting with PocketLedger via WhatsApp.

## Responsibilities
- Receives inbound webhooks from the Twilio/Meta WhatsApp Business API.
- Validates the `X-Twilio-Signature` HMAC-SHA1 header to ensure requests are authentic.
- Routes validated text messages and voice notes to the Core Ledger & Evidence Engine.
- Never interacts directly with the database or retains personally identifiable information (PII).

## Running Locally

```bash
npm install
npm run dev
```

Ensure you have copied `.env.example` to `.env` and populated it with your Twilio Auth Token and the URL of the Ledger Engine.
