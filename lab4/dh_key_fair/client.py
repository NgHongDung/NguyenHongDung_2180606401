from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

def generate_client_key_pair(parameters):
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

def derive_shared_key(private_key, server_public_key):
    shared_key = private_key.exchange(server_public_key)
    return shared_key

def main():
    # Load server's public key
    with open("server_public_key.pem", "rb") as f:
        server_public_key = serialization.load_pem_public_key(f.read()) 
    
    # Get DH parameters from server's public key
    parameters = server_public_key.parameters()
    
    # Generate client's DH key pair
    private_key, public_key = generate_client_key_pair(parameters)
    
    # Derive shared secret using client's private key and server's public key
    shared_key = derive_shared_key(private_key, server_public_key)
    
    print("Shared Secret:", shared_key.hex())

if __name__ == "__main__":
    main()
