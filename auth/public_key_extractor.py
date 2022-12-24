from Crypto.PublicKey import RSA

def exctract_public_key(private_key):
    # Extracts public key from private
    keyPriv = RSA.importKey(private_key) 
    public_key = keyPriv.publickey().exportKey('PEM')
    return public_key