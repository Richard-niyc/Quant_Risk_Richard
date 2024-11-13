import time
import requests
from web3 import Web3
import json

class AlchemyTransactionMonitor:
    def __init__(self, alchemy_http_url, uniswap_router_address, router_abi):
        # Connect to Ethereum mainnet via HTTP
        self.w3 = Web3(Web3.HTTPProvider(alchemy_http_url))
        if not self.w3.is_connected():
            raise ConnectionError("Unable to connect to Ethereum network.")

        # Load Uniswap V3 router contract address
        self.uniswap_router_address = Web3.to_checksum_address(uniswap_router_address)

        # Uniswap V3 router ABI, which is loaded in 'main'
        self.uniswap_router_abi = router_abi
            
        # Initialize contract instance
        self.uniswap_router_contract = self.w3.eth.contract(
            address=self.uniswap_router_address,
            abi=self.uniswap_router_abi
        )

        # Alchemy HTTP URL
        self.alchemy_http_url = alchemy_http_url

    def get_pending_transactions(self, retries=5, delay=2):
        # Using eth_getBlockByNumber with the "pending" block tag
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getBlockByNumber",
            "params": ["pending", True],
            "id": 1
        }

        for attempt in range(retries):
            try:
                response = requests.post(self.alchemy_http_url, json=payload, timeout=10)
                response.raise_for_status()
                result = response.json().get("result", {}).get("transactions", [])
                return result
            except requests.exceptions.RequestException as e:
                print(f"Error fetching pending transactions: {e}")
                print(f"Retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})")
                time.sleep(delay)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON response: {e}")
                break
    
        print("Failed to retrieve pending transactions after multiple attempts.")
        return []

    def monitor_pending_transactions(self):
        print("Monitoring pending transactions on Uniswap...")
        try:
            while True:
                # Retrieve pending transactions from Alchemy
                pending_transactions = self.get_pending_transactions()
        
                for tx_receipt in pending_transactions:
                    # Check if 'transactionHash' is present
                    if "hash" in tx_receipt:
                        try:
                            tx_hash = tx_receipt["hash"]
                            tx = self.w3.eth.get_transaction(tx_hash)
                            self.decode_transaction(tx)
                        except Exception as e:
                            print(f"Error processing transaction {tx_hash}: {e}")
                    else:
                        print("Transaction does not contain 'hash' key, skipping.")
                
                # Rate limiting to avoid overwhelming the provider
                time.sleep(2)
        except KeyboardInterrupt:
            print("Monitoring stopped by user.")

    def decode_transaction(self, tx):
        try:
            # Check if transaction is directed to the Uniswap router
            if tx["to"] != self.uniswap_router_address:
                #print("Skipping non-Uniswap transaction.")
                return
    
            # Decode the transaction input
            func_obj, func_params = self.uniswap_router_contract.decode_function_input(tx["input"])
            print(f"Decoded Transaction: {func_obj.fn_name} with parameters {func_params}")
    
            # Handle multicall transactions separately
            if func_obj.fn_name == "multicall":
                for call_data in func_params['data']:
                    try:
                        sub_func_obj, sub_func_params = self.uniswap_router_contract.decode_function_input(call_data)
                        print("Decoding multicall transaction...")
                        print(f"  Sub-call: {sub_func_obj.fn_name} with parameters {sub_func_params}")
                    except Exception as e:
                        print("Error decoding sub-call in multicall transaction:", e)

            else:
                # Process other types of transactions
                # Additional logic for other transaction types can be added here
                pass
    
        except Exception as e:
            print(f"Error decoding transaction input: {e}")

# Example Usage:
if __name__ == "__main__":
    YOUR_ALCHEMY_API_KEY = "jWUkgPqjx-Tk3W0DFm7drmMqx8pXNo0V"
    YOUR_ETHERSCAN_API_KEY = "79BRD8M6PUTES9DEVH92WI5PWC46MVI4FB"
    uniswap_router_address = "0xE592427A0AEce92De3Edee1F18E0157C05861564"

    alchemy_http_url = "https://eth-mainnet.alchemyapi.io/v2/" + YOUR_ALCHEMY_API_KEY
    ABI_URL = "https://api.etherscan.io/api?chainid=1&module=contract&action=getabi&address=" + uniswap_router_address + "&apikey=" + YOUR_ETHERSCAN_API_KEY
    
    # Load Uniswap V3 router ABI
    try:
        response = requests.get(ABI_URL).json()
        router_abi = json.loads(response['result'])
    except Exception as e:
        print(f"Failed to load ABI: {e}")
        exit(1)

    monitor = AlchemyTransactionMonitor(alchemy_http_url, uniswap_router_address, router_abi)
    monitor.monitor_pending_transactions()




