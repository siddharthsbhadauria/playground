import logging
import pandas as pd
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from io import BytesIO
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# AES block size
BLOCK_SIZE = 16

def initialize_key_vault(kv_url, client_id, client_secret, tenant_id):
    """
    Initialize Azure Key Vault with ClientSecretCredential
    """
    try:
        credential = ClientSecretCredential(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
        client = SecretClient(vault_url=kv_url, credential=credential)
        logger.info("Successfully initialized Azure Key Vault client")
        return client
    except Exception as e:
        logger.error(f"Error initializing Azure Key Vault: {e}")
        raise

def get_dek(client, dek_id, kek_id):
    """
    Retrieve and decrypt the Data Encryption Key (DEK) using the Key Encryption Key (KEK)
    """
    try:
        # Retrieve encrypted DEK from Azure Key Vault
        encrypted_dek = client.get_secret(dek_id).value
        encrypted_dek_bytes = base64.b64decode(encrypted_dek)

        # Retrieve KEK and unwrap the DEK
        kek_secret = client.get_secret(kek_id).value
        kek_private_key_data = base64.b64decode(kek_secret)

        # Load KEK and unwrap DEK
        private_key = serialization.load_pem_private_key(
            kek_private_key_data,
            password=None,
            backend=default_backend(),
        )

        dek = private_key.decrypt(
            encrypted_dek_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        logger.info("Successfully retrieved and decrypted DEK")
        return dek
    except Exception as e:
        logger.error(f"Error retrieving or decrypting DEK: {e}")
        raise

def encrypt_data(data, schema_info, dek):
    """
    Encrypt specific columns in the given data based on schema info
    """
    try:
        # Load the data as a DataFrame
        data_io = BytesIO(data)
        df = pd.read_csv(data_io)

        # Identify columns to encrypt
        columns_to_encrypt = [schema['Column Name'] for schema in schema_info if schema.get("PII", "N") == "Y" or schema.get("Masking Required", "N") == "Y"]

        # Set up the cipher with AES and CFB mode
        cipher = Cipher(algorithms.AES(dek), modes.CFB(BLOCK_SIZE * b'\x00'), backend=default_backend())
        encryptor = cipher.encryptor()

        # Encrypt specified columns
        for column in columns_to_encrypt:
            df[column] = df[column].apply(lambda x: base64.b64encode(encryptor.update(x.encode())).decode())

        encrypted_data = df.to_csv(index=False)
        logger.info("Data encryption successful")
        return encrypted_data
    except Exception as e:
        logger.error(f"Error encrypting data: {e}")
        raise

def decrypt_data(encrypted_data, schema_info, dek):
    """
    Decrypt specific columns in the given data based on schema info
    """
    try:
        # Load encrypted data into a DataFrame
        data_io = BytesIO(encrypted_data.encode())
        df = pd.read_csv(data_io)

        # Identify columns to decrypt
        columns_to_decrypt = [schema['Column Name'] for schema in schema_info if schema.get("PII", "Y") == "Y" or schema.get("Masking Required", "N") == "Y"]

        # Set up the cipher with AES and CFB mode
        cipher = Cipher(algorithms.AES(dek), modes.CFB(BLOCK_SIZE * b'\x00'), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt specified columns
        for column in columns_to_decrypt:
            df[column] = df[column].apply(lambda x: decryptor.update(base64.b64decode(x.encode())).decode())

        decrypted_data = df.to_csv(index=False)
        logger.info("Data decryption successful")
        return decrypted_data
    except Exception as e:
        logger.error(f"Error decrypting data: {e}")
        raise

def main():
    # Azure Key Vault credentials and URLs
    KV_URL = "<your-key-vault-url>"
    CLIENT_ID = "<your-client-id>"
    CLIENT_SECRET = "<your-client-secret>"
    TENANT_ID = "<your-tenant-id>"

    # Data Encryption Key and Key Encryption Key IDs from Key Vault
    DEK_ID = "<your-dek-id>"
    KEK_ID = "<your-kek-id>"

    # Initialize the Key Vault client
    client = initialize_key_vault(KV_URL, CLIENT_ID, CLIENT_SECRET, TENANT_ID)

    # Retrieve and decrypt the DEK
    dek = get_dek(client, DEK_ID, KEK_ID)

    # Sample CSV data (as bytes) for encryption
    sample_csv = b"""Col1,Col2,Col3
John,123,abc
Jane,456,xyz
"""

    # Example schema information
    schema_info = [
        {
            "Column Name": "Col1",
            "PII": "Y",
            "Masking Required": "N",
        },
        {
            "Column Name": "Col2",
            "PII": "N",
            "Masking Required": "Y",
        },
    ]

    try:
        # Encrypt data
        encrypted_data = encrypt_data(sample_csv, schema_info, dek)
        logger.info("Encrypted Data:\n" + encrypted_data)

        # Decrypt data
        decrypted_data = decrypt_data(encrypted_data, schema_info, dek)
        logger.info("Decrypted Data:\n" + decrypted_data)

    except Exception as e:
        logger.error(f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    main()
