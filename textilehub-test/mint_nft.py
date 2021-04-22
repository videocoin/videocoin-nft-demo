import os
import json
import argparse
import requests
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

from pprint import pprint
from decimal import Decimal


def get_contract(self, address, abi_fn):
    with open(abi_fn) as f:
        info_json = json.load(f)
        contract_abi = info_json['abi']
        return self.w3.eth.contract(address=self.w3.toChecksumAddress(address), abi=contract_abi)

parser = argparse.ArgumentParser(description='vidnft testing', argument_default=argparse.SUPPRESS)
parser.add_argument("-c", "--contract",  type=str, help="contract address", default="0x71f906422138478E9FF633ccE791E596679a67a7")
parser.add_argument("-t", "--token", type=int, help="token id", default=None)
parser.add_argument("-u", "--uri", type=str, help="uri", default=None)

args = parser.parse_args()

privateKey=os.environ.get("PRIVATE_KEY")
#blockchain_uri = "https://mainnet.infura.io/v3/" + os.environ.get("WEB3_INFURA_PROJECT_ID")
blockchain_uri = "https://rinkeby.infura.io/v3/" + os.environ.get("WEB3_INFURA_PROJECT_ID")

w3 = Web3(Web3.HTTPProvider(blockchain_uri))
print("Current block {}".format(w3.eth.blockNumber))

acct = w3.eth.account.privateKeyToAccount(privateKey)
print(acct.address)    

f = open("VidNft721.json")
info_json = json.load(f)

contract_abi  = info_json['abi']
vidnft = w3.eth.contract( address=args.contract, abi=contract_abi  )

pprint(vidnft.functions)
construct_txn = vidnft.functions.mint( acct.address, int(args.token)).buildTransaction({
    'from': acct.address,
    'nonce': w3.eth.getTransactionCount(acct.address),
    'gas': 500000,
    'gasPrice': w3.toWei('21', 'gwei')})
signed = acct.signTransaction(construct_txn)
tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
print("mint tx-hash {}".format(tx_hash.hex()))
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print("Transaction receipt mined:")
pprint(dict(receipt))
print("\nWas transaction successful?")
print(receipt["status"])

seturi_txn = vidnft.functions.setTokenURI(args.token, args.uri).buildTransaction({
    'from': acct.address,
    'nonce': w3.eth.getTransactionCount(acct.address),
    'gas': 500000,
    'gasPrice': w3.toWei('21', 'gwei')})
signed = acct.signTransaction(seturi_txn)
tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
print("mint tx-hash {}".format(tx_hash.hex()))
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print("Transaction receipt mined:")
pprint(dict(receipt))
print("\nWas transaction successful?")
pprint(receipt["status"])
