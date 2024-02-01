#This is an example file for how to create a deployment on AkashNetwork
import subprocess
import json
import time
import os
import requests
import random
import sys
from akash_main import create_wallet, create_and_publish_cert, create_deployment, close_deployment, get_wallet_address, publish_cert

# Set the AKASH_NET variable and get data from URLs
akash_net = "https://raw.githubusercontent.com/akash-network/net/main/mainnet"
chain_id = requests.get(f"{akash_net}/chain-id.txt").text.strip()
rpc_nodes = requests.get(f"{akash_net}/rpc-nodes.txt").text.splitlines()
akash_node = random.choice(rpc_nodes)

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

# Set your wallet password (Make sure to keep it secure)
password = 'Password1234!'
print('test')
# Create and fund a wallet
#create_wallet(password)

# Create and publish a certificate
#publish_cert(password)
#print('cert created')

#time.sleep(10)
print('test:', get_wallet_address(password))


#time.sleep(30)
# Create a deployment and store the relevant information
def create_and_manage_deployment(password):
    # Create a deployment
    akash_server_id, port, connect_ip, akash_provider_address = create_deployment(password)
    time.sleep(10)
    print(akash_server_id, port, connect_ip, akash_provider_address)
    # Manage the deployment
    # You can add more logic here to interact with the deployed server as needed

    # Close or delete the deployment when done
    close_deployment(akash_server_id, password)

# Call the function to create and manage a deployment
create_and_manage_deployment(password)