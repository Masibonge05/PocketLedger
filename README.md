# PocketLedger

**Financial Identity for Informal Traders**

PocketLedger is a WhatsApp-native platform designed to bring financial legibility to the informal economy. Millions of informal micro-enterprises—like spaza shops, street vendors, and township salons—operate entirely in cash. Because they leave no digital footprint, they are functionally invisible to formal financial institutions, meaning working capital, supplier financing, and insurance are routinely denied. 

PocketLedger solves this by wrapping a financial-recording layer around the tool these merchants already trust and use daily: WhatsApp.

## How It Works

1. **WhatsApp Native Interface**
   Merchants interact with PocketLedger entirely through a WhatsApp bot. There are no new apps to download or complex interfaces to learn. They can access a simple, numbered menu to log sales, record stock, or report wastage.

2. **Multilingual & Accessible**
   The platform supports 18 African and international languages. For merchants with low literacy, PocketLedger accepts Voice Notes. Merchants can simply speak their transactions, and the system handles the rest.

3. **AI Transaction Parsing**
   Merchants log transactions in natural language (e.g., "I sold 10 tomatoes for R10 each"). PocketLedger's AI layer instantly extracts the product, quantity, and price, updating the merchant's ledger and inventory in real time.

4. **Business Health Score**
   Every logged transaction builds the merchant's dynamic Business Health Score. This score proves their business is active and generating consistent revenue, acting as an alternative credit rating.

5. **Multi-Layered Validation & Blockchain Anchoring**
   To ensure the data is trustworthy for lenders:
   - **AI Checks:** Validates the plausibility of transactions.
   - **Receipt Vision:** Merchants can upload photos of supplier receipts, which the AI scans and verifies against their logged stock.
   - **Blockchain:** Every validated transaction is cryptographically hashed and anchored on-chain via a smart contract. This provides mathematically verified proof that the financial history is immutable and tamper-proof.

6. **The Financial Identity Passport**
   Merchants can generate professional digital invoices for their customers and pull full financial statements. When applying for loans or supplier financing, this verified statement acts as their "Financial Identity Passport," proving they are a bankable business.

## Project Structure

- **`ledger-engine/`**: The core FastAPI backend. Handles incoming webhooks, natural language parsing, database operations, and blockchain anchoring.
- **`dashboard/`**: A Streamlit application built for lenders, NGOs, and administrators to view the aggregated, verified data and Business Health Scores of merchants on the platform.
- **`smart-contracts/`**: Solidity contracts deployed to the blockchain used to anchor transaction hashes and establish a tamper-proof audit trail.
