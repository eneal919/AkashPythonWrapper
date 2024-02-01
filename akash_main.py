import subprocess
import os
import requests
import random
import pexpect
import json
import re
import time
import logging
import json
from flask import jsonify

#Importing the path
working_dir = os.path.dirname(os.path.realpath(__file__))

# SET THE PASSWORD YOU WANT TO BE USED FOR AKASH HERE
password = 'ENTERYOURPASSHERE'

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


#creates a deployment on Akash network
def akash_create_deployment(password):
  akash_create_deployment1=f'{working_dir}/akash-client/provider-services tx deployment create {working_dir}/deploy.yml --from myWallet --chain-id akashnet-2 --node {akash_node} --chain-id akashnet-2 --gas auto --gas-prices 0.025uakt --gas-adjustment 1.15 --sign-mode amino --home {working_dir}/.akash'
  child = pexpect.spawn(akash_create_deployment1)
  child.expect('Enter keyring passphrase:')
  child.sendline(password)
  child.expect('confirm transaction before signing and broadcasting')
  child.sendline('Y')
  child.sendline('')
  child.expect(pexpect.EOF)
  print(child.before.decode())
  output = (child.before.decode())
  json_match = re.search(r'\{.*\}', output)
  if json_match:
    json_output = json_match.group()
    try:
      data = json.loads(json_output)
      raw_log = data.get('raw_log', '')
      dseq_match = re.search(r'"dseq","value":"(\d+)"', raw_log)
      if dseq_match:
        dseq = dseq_match.group(1)
        print('Created Akash Server with DSEQ:', dseq)
        return dseq

      else:
        print("no dseq found")
    except json.JSONDecodeError:
      print("Invalid JSON output")
  else:
    print("no json found")

# close_deployment uses a Akash dseq to close a deployment  
def close_deployment(dseq,password):
  close_deployment1=f'{working_dir}/akash-client/provider-services tx deployment close --dseq {dseq} --from myWallet --home {working_dir}/.akash'
  child = pexpect.spawn(close_deployment1)
  child.expect('Enter keyring passphrase:')
  child.sendline(password)
  child.expect('confirm transaction before signing and broadcasting')
  child.sendline('Y')
  child.sendline('')
  child.expect(pexpect.EOF)
  #print(child.before.decode())
  print('Akash server stopped DSEQ(ServerID): ', dseq)

def akash_accept_lowest_bid(dseq,wallet_address):
  akash_accept_lowest_bid1 = f'{working_dir}/akash-client/provider-services query market bid list --owner={wallet_address} --dseq {dseq} --state=open'
  child = pexpect.spawn(akash_accept_lowest_bid1)
  child.expect(pexpect.EOF)

  # Capture the output
  output = child.before.decode()
  #print(output)  # For debugging

  # Regular expression pattern to extract bid information
  # Updated pattern to match floating-point numbers in the bid amount
  pattern = re.compile(r'owner: (\S+).*?amount: "([\d\.]+)"', re.DOTALL)

  # Find all matches
  matches = pattern.findall(output)
  #print("Matches found:", matches)  # For debugging

  # Initialize variables to track the lowest bid and its owner
  lowest_bid_amount = None
  lowest_bid_owner = None

  # Iterate over all matches to find the lowest bid
  for match in matches:
      owner, amount = match
      amount = float(amount)  # Convert amount to float for comparison

      # Update lowest bid and owner if this bid is lower than the current lowest, or if it's the first bid
      if lowest_bid_amount is None or amount < lowest_bid_amount:
          lowest_bid_amount = amount
          lowest_bid_owner = owner

  # Return the owner of the lowest bid
  if lowest_bid_owner:
      print('Akash Cheapest provider:', lowest_bid_owner)
      return lowest_bid_owner

  else:
      print("Error No Hosting bids found, You might want to try again in a few seconds")

def akash_execute_bid(dseq, provider,password):
  # Ensure that dseq is an integer and provider is a string
  dseq_int = int(dseq)
  if not isinstance(dseq_int, int) or not isinstance(provider, str):
      print("Error: Invalid types for dseq or provider")
      print(f"dseq type: {type(dseq)}, provider type: {type(provider)}")
      print(f"dseq value: {dseq}, provider value: {provider}")
      return

  akash_execute_bid1 = f'{working_dir}/akash-client/provider-services tx market lease create --dseq {dseq} --provider {provider} --from myWallet --node https://rpc.akashnet.net:443 --chain-id akashnet-2 --home {working_dir}/.akash'
  child = pexpect.spawn(akash_execute_bid1)

  try:
      child.expect('Enter keyring passphrase:', timeout=30)
      print("waiting to execute")
      child.sendline(password)
      print('password sent')
      print("Output after sending password:", child.before.decode())  # Debugging print
      child.expect('confirm transaction before signing and broadcasting', timeout=30)
      child.sendline('Y')
      print('yes sent')
      print("Output after sending 'Y':", child.before.decode())  # Debugging print
      child.expect(pexpect.EOF, timeout=30)
      print("execute bid")
  except pexpect.exceptions.EOF:
      print("pexpect EOF error occurred execute")
      print("Output at EOF:", child.before.decode())  # Debugging print
  except pexpect.exceptions.TIMEOUT:
      print("pexpect TIMEOUT error occurred")
  except Exception as e:
      print(f"An error occurred: {e}")

def akash_send_manifest(dseq, provider,password):
  # Convert dseq to an integer
  try:
      dseq_int = int(dseq)
  except ValueError:
      print(f"Error: dseq must be an integer. Received: {dseq}")
      return

  # Ensure owner is a string
  if not isinstance(provider, str):
      print("Error: Owner must be a string")
      return

  # Prepare the command
  manifest_command = f'{working_dir}/akash-client/provider-services send-manifest deploy.yml --dseq {dseq} --provider {provider} --from myWallet --node https://rpc.akashnet.net:443 --home {working_dir}/.akash'
  child = pexpect.spawn(manifest_command)

  try:
      child.expect('Enter keyring passphrase:', timeout=30)
      print("waiting to send manifest")
      child.sendline(password)  
      child.expect('status:       PASS', timeout=30)
      child.expect(pexpect.EOF, timeout=30)
      print("manifest sent")
  except pexpect.exceptions.EOF:
      print("pexpect EOF error occurred manifest")
  except pexpect.exceptions.TIMEOUT:
      print("pexpect TIMEOUT error occurred")
  except Exception as e:
      print(f"An error occurred manifest: {e}")


def akash_get_server_details(dseq, provider,password):
  get_server_details_command = f'{working_dir}/akash-client/provider-services lease-status --provider {provider} --dseq {dseq} --from myWallet --node https://rpc.akashnet.net:443 --home {working_dir}/.akash'
  child = pexpect.spawn(get_server_details_command)
  try:
      child.expect('Enter keyring passphrase:', timeout=30)
      child.sendline(password) 
      child.expect(pexpect.EOF, timeout=30)
      output = child.before.decode()
      print("Getting Forwarded Ports")
      data = json.loads(output)
      # Adjusted to match your JSON structure
      # Extract the external port
      port = None
      service_name = 'service-1'  # Adjust the service name if needed
      if 'forwarded_ports' in data and service_name in data['forwarded_ports']:
          port = data['forwarded_ports'][service_name][0].get('externalPort', None)
      # Extract connect IP
      connect_ip = None
      if 'services' in data and service_name in data['services'] and 'uris' in data['services'][service_name]:
          connect_ip = data['services'][service_name]['uris'][0]
      print("Here are your server details", flush=True)
      print(f"Port: {port}")
      print(f"Connect IP: {connect_ip}")
      return port, connect_ip
  except Exception as e:
      logging.info('Error: Failed to get server details' + str(e))
      print('Failed to get server details')
      return None, None
#WIP BELOW
def internal_get_logs(dseq,provider,password):
  child = f'{working_dir}/akash-client/provider-services lease-logs --provider {provider} --dseq {dseq} --from myWallet --node https://rpc.akashnet.net:443'
  child = pexpect.spawn(child)
  data = child.before.decode()
  child.expect(pexpect.EOF)
  return jsonify(data)

def create_deployment(password):
  try:
    wallet_address = get_wallet_address(password)
    akash_server_id=akash_create_deployment(password)
    time.sleep(11)
    akash_provider_address=akash_accept_lowest_bid(akash_server_id,wallet_address)
    akash_execute_bid(akash_server_id, akash_provider_address,password)
    time.sleep(10)
    akash_send_manifest(akash_server_id, akash_provider_address,password)
    time.sleep(10)
    port, connect_ip = akash_get_server_details(akash_server_id, akash_provider_address,password)
    print('Combined Func: Server Details checked',)
  except KeyError as e:
    logging.info('FAILED create server combined function failed with error: ', e)
  else:
    return akash_server_id, port, connect_ip, akash_provider_address


def publish_cert(password):
  gen_cert1=f'{working_dir}/akash-client/provider-services tx cert publish client --from myWallet --home {working_dir}/.akash'
  child = pexpect.spawn(gen_cert1)
  child.expect('Enter keyring passphrase:')
  child.sendline(password)
  child.sendline('y')
  child.sendline('')
  child.expect(pexpect.EOF)
  print(child.before.decode())
def gen_cert(password):
  gen_cert1=f'{working_dir}/akash-client/provider-services tx cert generate client --from myWallet --home {working_dir}/.akash'
  child = pexpect.spawn(gen_cert1)
  child.expect('Enter keyring passphrase:')
  child.sendline(password)
  child.sendline('')
  child.expect('')
  child.expect(pexpect.EOF)
  print(child.before.decode())


def create_and_publish_cert(password):
    gen_cert(password)
    print('Cert created')
    publish_cert(password)
    print('Cert published')

def get_wallet_address(password):
  #Run akash client and get myWallet Address
  wallet_address_command = f'{working_dir}/akash-client/provider-services keys show myWallet --home {working_dir}/.akash'
  child = pexpect.spawn(wallet_address_command)

  #send wallet password
  child.expect('Enter keyring passphrase:')
  child.sendline(password)
  
  #Find wallet address
  child.expect(pexpect.EOF)
  data = child.before.decode()
  pattern = r"address: (\w+)"
  match = re.search(pattern, data, re.IGNORECASE | re.DOTALL)
  address = match.group(1)
  
  return address


def create_wallet(password):
  # Run akash provider services in pexpect
  init_wallet1= f'{working_dir}/akash-client/provider-services keys add myWallet --home {working_dir}/.akash'
  child = pexpect.spawn(init_wallet1)

  #create and enter keyring passphrase
  child.expect('Enter keyring passphrase:')
  child.sendline(password)
  child.expect('Re-enter keyring passphrase:')
  child.sendline(password)

  #Get wallet address and save private keys to a file 
  child.expect(pexpect.EOF)
  data = child.before.decode()
  print('Akash Wallet Created and backup saved to keys/myWallet-Backup.txt, Your Address Akash is:', get_wallet_address(password))  
  with open(f'{working_dir}/keys/myWallet-Backup.txt', 'w') as file:
    file.write(data)





#create_deployment(password)
#close_deployment(str(14720988),password)
#get_wallet_address(password)
