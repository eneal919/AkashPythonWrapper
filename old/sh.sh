cp -r /home/runner/AKTCreateAPI/akashfiles/* /home/runner/.akash
export PATH=$PATH:~/.akash/
export AKASH_KEY_NAME=myWallet
export AKASH_KEYRING_BACKEND=os
export AKASH_NET="https://raw.githubusercontent.com/akash-network/net/main/mainnet"
export AKASH_CHAIN_ID="$(curl -s "$AKASH_NET/chain-id.txt")"
export AKASH_NODE="$(curl -s "$AKASH_NET/rpc-nodes.txt" | shuf -n 1)"
export AKASH_GAS=auto
export AKASH_GAS_ADJUSTMENT=1.15
export AKASH_GAS_PRICES=0.025uakt
export AKASH_SIGN_MODE=amino-json