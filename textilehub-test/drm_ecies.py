import argparse
from ecies import encrypt, decrypt

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='VidNft DRM testing.')
    parser.add_argument('-s', '--receiver_privatekey',type=str, default="", help='decode with private key')
    parser.add_argument('-d', '--drm_key',type=str, default="", help='Encrypted Content Encryption key')
    
    args = parser.parse_args()

    #drm_key = encrypt(args.receiver_pubkey, bytes(args.cenc, 'utf-8'))
    #print(drm_key.hex())
    decrypted_encryption_key = decrypt(args.receiver_privatekey, bytes.fromhex(args.drm_key))
    print(decrypted_encryption_key)
