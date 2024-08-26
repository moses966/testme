from fastapi import Depends, HTTPException, APIRouter, status
from datetime import timedelta
from ape import networks, Project, accounts
from eth_account.messages import encode_defunct
from web3 import Web3
from web3.auto import w3
from ape.exceptions import TransactionError
from web3.exceptions import TransactionNotFound
import logging
from . import schemas



# Create router instance
router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Hello, World!"}

@router.get("/get-string", response_model=schemas.GetStringResponse)
async def get_string():
    """
    - Endpoint for interacting with the smart contract to retrieve a string value.
    - Connects to the specified contract on the Arbitrum Sepolia network.
    """
    contract_address = '0x312835d3B01D7c472E00d4678240387EB44303ab'  # Replace this value if necessary
    network_name = 'arbitrum:sepolia'

    try:
        with networks.parse_network_choice(network_name) as net:
            artifacts = Project("/home/moses/fastapi-sample/smart-contracts")
            contract = artifacts.Greeting.at(contract_address)
            result = contract.greeting()
            return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    



@router.post("/update-string")
async def update_string(request: schemas.UpdateStringRequest):
    """
    Verify the signature and process the transaction in the smart contract.
    """
    #contract_address = '0x312835d3B01D7c472E00d4678240387EB44303ab'
    network_url = 'https://arb-sepolia.g.alchemy.com/v2/DuDJETvLkjSIr8a_EM89WeUlsM5WIq0X'
    
    try:
        # Initialize Web3 with a provider
        web3 = Web3(Web3.HTTPProvider(network_url))

        # Verify the signature
        encoded_message = Web3.solidity_keccak(['string'], [request.message])
        recovered_address = web3.eth.account.recoverHash(encoded_message, signature=request.signature)

        if recovered_address.lower() != request.address.lower():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")

        # Decode the signed transaction and send it to the network
        signed_tx = request.signedTx
        tx_hash = web3.eth.send_raw_transaction(signed_tx)

        # Poll for the transaction receipt
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt.status != 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transaction failed")

        return {"transaction_hash": tx_hash.hex()}

    except TransactionNotFound as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))