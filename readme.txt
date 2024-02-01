Akash Network Provider Services Python Wrapper

This Python script serves as a wrapper for Akash Network Provider Services, allowing you to create and manage deployments. Below are the core functions and their usage.

Functions

1. create_deployment(password)
This function automates the process of creating an Akash deployment. It performs the following steps:

- Creates a deployment.
- Accepts the lowest bid.
- Executes the bid.
- Sends the deployment manifest.
- Retrieves server details.
Usage:

akash_server_id, port, connect_ip, akash_provider_address = create_deployment(password)

2. close_deployment(dseq, password)
Use this function to close a deployment based on its DSEQ (Deployment Sequence ID).

Usage:

close_deployment(dseq, password)

3. akash_accept_lowest_bid(dseq, wallet_address)
This function retrieves the lowest bid for a specific deployment and returns the provider's wallet address.

Usage:

lowest_bid_owner = akash_accept_lowest_bid(dseq, wallet_address)

4. akash_execute_bid(dseq, provider, password)
Execute the bid for a specific deployment with the chosen provider.

Usage:

akash_execute_bid(dseq, provider, password)

5. akash_send_manifest(dseq, provider, password)
Send the deployment manifest to the chosen provider.

Usage:

akash_send_manifest(dseq, provider, password)

6. akash_get_server_details(dseq, provider, password)
Retrieve server details, including the port and connect IP, for a deployed service.

Usage:

port, connect_ip = akash_get_server_details(dseq, provider, password)

7. create_wallet(password)
This function creates an Akash wallet and saves the backup to a file.

Usage:

create_wallet(password)

8. get_wallet_address(password)
Get the wallet address associated with your Akash wallet.

Usage:

wallet_address = get_wallet_address(password)

9. create_and_publish_cert(password)
Create and publish an Akash certificate.

Usage:

create_and_publish_cert(password)

Configuration
Before using these functions, ensure you have set up the necessary environment variables and provided your password in the script. Additionally, adjust any other configuration parameters according to your requirements.

For advanced usage and additional functions within the script, refer to the script itself and the Akash Network documentation.

# Set environment variables
os.environ['AKASH_KEY_NAME'] = 'myWallet'
os.environ['AKASH_KEYRING_BACKEND'] = 'os'
os.environ['AKASH_NET'] = "https://raw.githubusercontent.com/akash-network/net/tree/main/mainnet"
os.environ['AKASH_CHAIN_ID'] = 'akashnet-2'
os.environ['AKASH_NODE'] = "https://rpc.akashnet.net:443"
os.environ['AKASH_GAS'] = 'auto'
os.environ['AKASH_GAS_ADJUSTMENT'] = '1.15'
os.environ['AKASH_GAS_PRICES'] = '0.025uakt'
os.environ['AKASH_SIGN_MODE'] = 'amino-json'