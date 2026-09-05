import os
import hashlib
from web3 import Web3
import logging

logger = logging.getLogger(__name__)

WEB3_PROVIDER_URI = os.environ.get("WEB3_PROVIDER_URI", "")
CONTRACT_ADDRESS = os.environ.get("CONTRACT_ADDRESS", "")
WALLET_PRIVATE_KEY = os.environ.get("WALLET_PRIVATE_KEY", "")

# Minimal ABI for what we need
CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "merchantID", "type": "string"},
            {"internalType": "bytes32", "name": "dataHash", "type": "bytes32"}
        ],
        "name": "logIdentityState",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "string", "name": "merchantID", "type": "string"}],
        "name": "getLatestState",
        "outputs": [
            {"internalType": "bytes32", "name": "", "type": "bytes32"},
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

def get_web3():
    if not WEB3_PROVIDER_URI:
        return None
    return Web3(Web3.HTTPProvider(WEB3_PROVIDER_URI))

def compute_state_hash(merchant_id: str, health_score: float, cumulative_revenue: float) -> bytes:
    # Compute SHA256(merchant_id + health_score + cumulative_revenue)
    payload = f"{merchant_id}{health_score}{cumulative_revenue}".encode('utf-8')
    return hashlib.sha256(payload).digest()

def submit_state_hash_to_chain(merchant_id: str, data_hash: bytes) -> str:
    """Submits the state hash to Sepolia. Returns transaction hash."""
    w3 = get_web3()
    if not w3 or not CONTRACT_ADDRESS or not WALLET_PRIVATE_KEY:
        logger.warning("Web3 not configured. Mocking transaction.")
        return "0xMockedTransactionHash12345"
        
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    account = w3.eth.account.from_key(WALLET_PRIVATE_KEY)
    
    nonce = w3.eth.get_transaction_count(account.address)
    
    tx = contract.functions.logIdentityState(merchant_id, data_hash).build_transaction({
        'chainId': 11155111, # Sepolia chain ID
        'gas': 2000000,
        'maxFeePerGas': w3.to_wei('2', 'gwei'),
        'maxPriorityFeePerGas': w3.to_wei('1', 'gwei'),
        'nonce': nonce,
    })
    
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=WALLET_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    return w3.to_hex(tx_hash)

def verify_hash_on_chain(merchant_id: str, expected_hash: bytes) -> bool:
    """Reads on-chain hash and compares to expected."""
    w3 = get_web3()
    if not w3 or not CONTRACT_ADDRESS:
        logger.warning("Web3 not configured. Mocking verification as True.")
        return True
        
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    
    try:
        onchain_hash, timestamp = contract.functions.getLatestState(merchant_id).call()
        return onchain_hash == expected_hash
    except Exception as e:
        logger.error(f"Error reading from chain: {e}")
        return False
