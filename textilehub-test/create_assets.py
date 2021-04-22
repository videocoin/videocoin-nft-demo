import sys
import ipfsApi
import json
import argparse
from pprint import pprint
from subprocess import call
from ecies import encrypt, decrypt
import shutil

def ffmpeg_encrypt(input, output, loglevel, encryption_key, encryption_id):
    call(["/usr/bin/ffmpeg", "-y", "-i", input, "-vcodec", "copy", "-acodec", "copy", "-encryption_scheme", "cenc-aes-ctr", "-loglevel", loglevel, "-encryption_key", encryption_key,
          "-encryption_kid", encryption_id, output])

def ffmpeg_getimage(input, output):
    call(["ffmpeg", "-hide_banner", "-loglevel", "info", "-y", "-ss", "4", "-i", input, "-an",  "-vframes", "1", output])

parser = argparse.ArgumentParser(description='VidNft testing.')
parser.add_argument('-i', '--input',type=str, default="", help='Input file')
parser.add_argument('-t', '--token',type=str, default="", help='Token ID hex string')
parser.add_argument('-n', '--name',type=str, default="Racing Horse", help='Name string')
parser.add_argument('-d', '--description',type=str, default="First Motion Picture 1878", help='Description string')
parser.add_argument('-g', '--gateway',type=str, default="", help='bucket url')
parser.add_argument('-e', '--encryption_key',type=str, default="76a6c65c5ea762046bd749a2e632ccbb", help='Encryption key')
parser.add_argument('-c', '--contract_address',type=str, default="0x71f906422138478E9FF633ccE791E596679a67a7", help='Contract address')
parser.add_argument('--encryption_kid',type=str, default="a7e61c373e219033c21091fa607bf3b8", help='Encryption key ID')
parser.add_argument('-r', '--receiver_pubkey',type=str, default="", help='Receiver Public Key')

args = parser.parse_args()

ipfs_prefix = "ipfs://"
image_name = "image.jpg"
output_name = "encrypted_" + args.input
ffmpeg_encrypt(args.input, output_name, "info", args.encryption_key, args.encryption_kid)
ffmpeg_getimage(args.input,  "image.jpg")

api = ipfsApi.Client('127.0.0.1', 5001)
resInput = api.add(args.input)
pprint(resInput)
print(resInput["Hash"])

resOut = api.add(output_name)
resImg = api.add(image_name)

data = {}
data['name'] = args.name
data['description'] = args.description
data['image'] = args.gateway + resImg["Hash"]
data['animation_url'] = args.gateway + resInput["Hash"]
data['external_link_encrypted'] = args.gateway + resOut["Hash"]
data['ipfs_image'] = ipfs_prefix + resImg["Hash"]
data['ipfs_animation_url'] = ipfs_prefix + resInput["Hash"]
data['ipfs_external_link_encrypted'] = ipfs_prefix + resOut["Hash"]

if args.receiver_pubkey:
    drm_key = encrypt(args.receiver_pubkey, bytes(args.encryption_key, 'utf-8'))
    data['drm_key'] = drm_key.hex()

with open(args.token, 'w') as outfile:
    json.dump(data, outfile, indent=2)

res_token_uri = api.add(args.token)

# copy files to assets
assets = "./assets/"
shutil.copy2(args.token, assets + res_token_uri["Hash"])
shutil.copy2(image_name, assets + resImg["Hash"])
shutil.copy2(args.input, assets + resInput["Hash"])
shutil.copy2(output_name, assets + resOut["Hash"])
#call([sys.executable, './vidnft_contract.py', "-a", args.contract_address, '-m', args.token])
