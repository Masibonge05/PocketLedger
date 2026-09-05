# PocketLedger Smart Contracts

This directory contains the Solidity smart contracts used for anchoring the PocketLedger state to the Ethereum Sepolia blockchain.

## Responsibilities
- The `PocketLedgerAnchor.sol` contract stores an immutable state hash for merchants.
- Emits events when states are anchored.
- Provides a view function for the dashboard to verify data integrity against the chain.
- Ensures strict access control (only authorized backend can write) and resistance to reentrancy and timestamp manipulation.

## Deployment & Verification

Ensure you have run `Slither` and `Mythril` to analyze the contract before deployment.

To deploy (example using Hardhat/Foundry, configure accordingly):
1. Copy `.env.example` to `.env` and add your Sepolia RPC URL and Private Key.
2. Deploy to the Sepolia testnet.
3. Update the `CONTRACT_ADDRESS` in the `ledger-engine`'s environment variables.
