# VID NFT Testing with Textile Hub

Steps
* Setup Textile Hub bucket
* Deploy VidNft721 contract on Rinkeby testnet
* Create Video Assests for VID NFT
* Upload Video Assets to Textile Hub/Filecoin
* Mint VID NFT
* Access the VID NFT using a dApp
* Retrieve the token URI and validate Integrity and DRM

## Clone the videocoin-nft-demo repo
```
git clone https://github.com/videocoin/videocoin-nft-demo
cd textilehub-test
```

## Setup Textile Hub bucket
Download and install the Textile Hub from the follwoing link:  
https://github.com/textileio/textile/releases/tag/v2.6.8  

Signup for the Textile Buckets   
https://textile.io/  

create an sub folder "assets" to hold video assets
```
 hub login
 hub bucket init
 hub buck link
```
hub login requires email based authenticaion.

### API Key based upload to Bucket
You can use either hub api manually or alternately, you can upload the files using node application. Node application uses  hub js script that inturn uses TextileIo's hub js library.

Example
```
cd hubjs
npm start ../assets/QmZ2d3be8b9jRcWmpXzBTgihKuRDZQiMqMN2xguv9bvcLq
```

## Deploy VidNft721 contract on Rinkeby testnet
This smart contract is tested with brownie-ethereum

### Setup brownie

https://eth-brownie.readthedocs.io/en/stable/install.html

Configure brownie-config.yaml to select the blockchain

Intall openzeppelin-contracts@3.4.0 for ERC721 and ERC1155 contracts
```
brownie pm install OpenZeppelin/openzeppelin-contracts@3.4.0
```

compile the contract
```
brownie compile
```

Add a test account. Example:
```
brownie accounts new account1
```
You will be prompted for a private key

Deploy contract and test it using brownie console. you need to set the infura project id for testnet, if used
```
export WEB3_INFURA_PROJECT_ID="XXXXXXXXXXXXXXXXX"
brownie console
```
In the brownie console load and activate the account
```
accounts.load("account1")
```
Deploy the contract. Supply the contract name(example: VidNftTest) and symbol(example: TST1).
```
VidNft721.deploy("VidNftTest", "TST1", {'from':accounts[0]})
```
Note the contract address. Example:  
0x71f906422138478E9FF633ccE791E596679a67a7

## Create Video Assests for VID NFT

Create video assets for the NFT using the create_assets script. Supply the input video. The script creates thumbnail image, encrypted video and token URI file for the NFT. The files are copied to assets sub-folder mapped to textile Hub

A temporary mechanism for generating CIDs, run ipfs. It is not required in the final env.
```
ipfs daemon
```
Example command: Supply the input file, token id and description.

```
python3 create_assets.py -i firstfilm.mp4 -t 3000 -n "my nft" -d "my cool nft"
```
Token URI contents example:
```
{
  "name": "Racing Horse",
  "description": "First Motion Picture 1878",
  "image": "https://hub.textile.io/ipns/bafzbeieigd...43yimwgzryvtnbj6rte/QmdDM1..kUv8",
  "animation_url": "https://hub.textile.io/ipns/bafzbe...nbj6rte/QmP6yiY...PM3",
  "external_link_encrypted": "https://hub.textile.io/ipns/bafz...bj6rte/Qma9...oaZgS",
  "ipfs_image": "ipfs://QmdDM1JFsDcSiBYefuUQ5kbiWTUegu2eGJPaiGx4mXkUv8",
  "ipfs_animation_url": "ipfs://QmP6yiY4kMrPiMnC3cemvpchXt3Rrm4kXbuGNacEfXgPM3",
  "ipfs_external_link_encrypted": "ipfs://Qma9FqzsG2dSx7b5ZmNkzqxfvYX9Aka9exRUPTDEZoaZgS",
  "drm_key": "04203ce14a6fcb2cd458...0550e6b4addce5e6167569cd"
}
```

## Upload Video Assets to Textile Hub/Filecoin
Upload the assets
```
cd assets
hub bucket push
```

Alternately use hubjs node application described previously.

## Mint VID NFT
use the script mint_nft.py  to mint a VID NFT. Supply token ID for the NFT with -t option and token uri with -u option.   

Set environment varibales to supply infura project ID and private key for sigming mint transactions.

```
export PRIVATE_KEY="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
export WEB3_INFURA_PROJECT_ID=AAAAAAAAAAAAAAAAAA
```

Example mint command.
```
python3 mint_nft.py -t 1730 -u https://hub.textile.io/ipns/bafzbeieigdvhfntbfkf7semdska5bxokinvs6oi43yimwgzryvtnbj6rte/QmZ2d3be8b9jRcWmpXzBTgihKuRDZQiMqMN2xguv9bvcLq
```
## Access the VID NFT using a dApp

### VideoCoin demo app
-- TODO --
### OpenSea Integratoin
* Setup your browser to enable metamask extension
* Setup metamask to use Rinkeby testnet
* go to https://opensea.io/get-listed
* Select "liveon testnet"
* Supply the VidNft721 contract address. Example 0x71f906422138478E9FF633ccE791E596679a67a7
The above step will create a page for the contract and enables viewing and trading options
https://testnets.opensea.io/collection/vidnfttest

OpenSea requires "setApprovalForAll" to be set by the token holder during listing. 

## Retrive the token URI and validate content integrity and DRM
Retireve the token URI from blockchain  
Example:
https://rinkeby.etherscan.io/address/0x99c968f667462d9b674e9aba38d6d6d2232456cb

Locate "Set Token URI" transaction for the minted token.
Select "Decode Input Data" option for the transaction.

Get the token URI for the token. 
Example:  
```
tokenId	uint256	1730
_uri	string	https://hub.textile.io/ipns/bafzbeieigdvhfntbfkf7semdska5bxokinvs6oi43yimwgzryvtnbj6rte/QmZ2d3be8b9jRcWmpXzBTgihKuRDZQiMqMN2xguv9bvcLq
```
Retrive the token data from the above link.

The token data can also be retrieved from the ipfs
```
ipfs://QmZ2d3be8b9jRcWmpXzBTgihKuRDZQiMqMN2xguv9bvcLq
```

### Check integrity and DRM
* Retrieve the drm data from the token URI
* Use the script drm_ecies.py to decrypt the drm data. You need to supply the private key corresponding to the public key used for creating DRM data.
* This step outputs the content encryption key.
* Use the content encryption key to decode the encrypted video asset using ffmpeg.

Example: Decrypt DRM data and retrieve content encryption key. You need to supply private key with -s option and DRM data with -d option
```
python3 drm_ecies.py -s <private key> -d <drm key from token uri>
```
outputs content deryption key on succesful decryption of DRM:

Decrypt the content using the encryption key used in the previous step.
```
ffmpeg  -decryption_key <decryption key> -i encrypted_firstfilm.mp4 -c:v copy -c:a copy test_dec.mp4
```