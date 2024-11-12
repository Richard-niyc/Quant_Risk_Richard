# Onchain Analytics

## Overview

This project is a Python script that monitors Uniswap pending transactions on the Ethereum mainnet. It uses Alchemy as an Ethereum node provider and Etherscan for retrieving the ABI of the Uniswap V3 router.

## Features

- Connects to the Ethereum network using Alchemy's HTTP API.
- Monitors pending transactions in real-time and decodes interactions with the Uniswap V3 Router.
- Handles Uniswap multicall transactions to decode each sub-call.
- Retry mechanism for improved reliability in network requests.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Libraries:
  - `requests`
  - `web3`
  - `json`
  - `time`

The following Python packages are required:

```sh
pip install web3 requests json time
```

### Running the Project

1. **Clone the Repository**

   ```sh
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **API Keys**:

   - Obtain an **Alchemy API Key**: Visit [Alchemy](https://www.alchemy.com/) to sign up and obtain an API key for accessing Ethereum Mainnet.
   - Obtain an **Etherscan API Key**: Visit [Etherscan](https://etherscan.io/) to sign up and obtain an API key for fetching the Uniswap router ABI.

3. **Update the script**:

   - Replace `YOUR_ALCHEMY_API_KEY` and `YOUR_ETHERSCAN_API_KEY` in the script with your actual API keys.

4. **Run the script**


## Class Initialization and Functions

### Class Initialization

The `AlchemyTransactionMonitor` class is initialized with the following:

- **Alchemy HTTP URL**: Connects to the Ethereum network through Alchemy's HTTP API.
- **Uniswap Router Address**: The contract address for the Uniswap V3 Router.
- **Uniswap Router ABI**: Loaded from Etherscan to decode Uniswap transactions.
- **Initialize contract instance**: Uses `w3.eth.contract` with router address and abi as input

### Functions

- **`get_pending_transactions()`**: Fetches pending transactions using the `eth_getBlockByNumber` method with the "pending" block tag.
- **`monitor_pending_transactions()`**: Monitors pending transactions on the Ethereum network in real-time.
- **`decode_transaction()`**: Checks if transaction is directed to the Uniswap V3 Router, decodes the transaction and handle multicall transactions.

### Output

You will see decoded transactions, including the function names and parameters used in the Uniswap V3 Router.

## Error Handling

- **Data Retrieval**: The code implements retry logic when attempting to retrieve pending transactions from the Alchemy API. If a request fails, it will retry up to a specified number of times (`retries=5`), with a delay between each attempt (`delay=2`). This helps mitigate temporary network issues or rate limiting by the API provider.

- **Rate Limiting**: The monitoring function includes a sleep interval (`time.sleep(2)`) after processing each batch of pending transactions. This helps prevent overwhelming the provider, particularly when querying the blockchain frequently. Adjust this rate limit according to your API rate limits to avoid throttling or bans.

- **Error Decoding Transactions**: The `decode_transaction` method includes error handling for both direct transactions and multicall sub-transactions, ensuring that if one transaction fails to decode, it does not prevent further processing.

## Important Notes

- **Alchemy and Etherscan Limits**: Ensure that your Alchemy and Etherscan accounts have enough API call limits to avoid being blocked.
- **Real-time Monitoring**: Monitoring pending transactions is resource-intensive and requires constant polling, so keep in mind potential API rate limitations and network usage.
- **Keyboard Interrupt**: The script can be safely stopped using `Ctrl + C`.

---

