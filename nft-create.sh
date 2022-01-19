#!/bin/sh

PYTHON_BINARY=python3.8
OWNER_WALLET=alice.pem
NFT_ATTRIBUTES_JSON=nft-create-args.json
GAS_LIMIT=8000000

PROXY="https://devnet-api.elrond.com"
CHAIN="D"

OWNER_ADDRESS=$(erdpy wallet pem-address $OWNER_WALLET)
set -ex
DATA=$($PYTHON_BINARY ./prepare-args.py nft-create $NFT_ATTRIBUTES_JSON)
erdpy tx new --pem $OWNER_WALLET --data $DATA --receiver $OWNER_ADDRESS --proxy $PROXY --recall-nonce --gas-limit $GAS_LIMIT --chain $CHAIN --send
