import os
import solcx
from web3 import Web3

def deploy():
    # Install solidity compiler
    solcx.install_solc('0.8.20')
    solcx.set_solc_version('0.8.20')

    contract_path = os.path.join("..", "smart-contracts", "contracts", "PocketLedgerAnchor.sol")
    
    with open(contract_path, 'r') as f:
        contract_source = f.read()

    print("Compiling contract...")
    compiled_sol = solcx.compile_source(
        contract_source,
        output_values=['abi', 'bin']
    )

    contract_id, contract_interface = compiled_sol.popitem()
    abi = contract_interface['abi']
    bytecode = contract_interface['bin']

    # Set up web3
    rpc_url = "https://sepolia.infura.io/v3/6c195b7a8b6047ecb23df6414afa100e"
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    if not w3.is_connected():
        print("Failed to connect to Sepolia testnet.")
        return

    print("Connected to Sepolia!")
    
    private_key = "0x98c8abcd23b73383ecae263797c4ab5fd265fec13a5f9e639d058869a0600e7d"
    account = w3.eth.account.from_key(private_key)
    print(f"Deploying from address: {account.address}")

    # Estimate gas
    PocketLedgerAnchor = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    nonce = w3.eth.get_transaction_count(account.address)
    
    print("Building transaction...")
    transaction = PocketLedgerAnchor.constructor().build_transaction({
        'chainId': 11155111,
        'gas': 2000000,
        'maxFeePerGas': w3.to_wei('10', 'gwei'),
        'maxPriorityFeePerGas': w3.to_wei('2', 'gwei'),
        'nonce': nonce,
    })

    print("Signing transaction...")
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

    print("Sending transaction...")
    txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print(f"Transaction sent! Hash: {w3.to_hex(txn_hash)}")

    print("Waiting for receipt...")
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    
    print(f"Contract deployed to: {txn_receipt.contractAddress}")

if __name__ == "__main__":
    deploy()
