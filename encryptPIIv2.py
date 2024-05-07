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

class DataEncryptor:
    def __init__(self, kv_url, client_id, client_secret, tenant_id):
        self.kv_url = kv_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id

        # Initialize Azure Key Vault client
        credential = ClientSecretCredential(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
        self.client = SecretClient(vault_url=kv_url, credential=credential)

    def _get_dek(self, dek_id, kek_id):
        """
        Retrieve and decrypt the Data Encryption Key (DEK) using the Key Encryption Key (KEK)
        """
        # Retrieve the encrypted DEK from Azure Key Vault
        encrypted_dek = self.client.get_secret(dek_id).value
        encrypted_dek_bytes = base64.b64decode(encrypted_dek)

        # Retrieve the KEK for unwrapping the DEK
        kek_secret = self.client.get_secret(kek_id).value
        kek_public_key = base64.b64decode(kek_secret)

        # Load the KEK (RSA 4096)
        private_key = serialization.load_pem_private_key(
            kek_public_key,
            password=None,
            backend=default_backend(),
        )

        # Unwrap the DEK using the KEK
        dek = private_key.decrypt(
            encrypted_dek_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        return dek

    def encrypt_data(self, data, schema_info, dek_id, kek_id):
        """
        Encrypt specific columns in the given data based on schema info
        """
        dek = self._get_dek(dek_id, kek_id)

        # Load the data as a DataFrame
        data_io = BytesIO(data)
        df = pd.read_csv(data_io)

        # Identify columns to encrypt based on schema info
        columns_to_encrypt = [schema['Column Name'] for schema in schema_info if schema.get("PII", "N") == "Y" or schema.get("Masking Required", "N") == "Y"]

        # Encrypt specified columns
        cipher = Cipher(algorithms.AES(dek), modes.CFB(BLOCK_SIZE * b'\x00'), backend=default_backend())
        encryptor = cipher.encryptor()

        for column in columns_to_encrypt:
            # Encrypt data and convert to base64 to keep it as string
            df[column] = df[column].apply(lambda x: base64.b64encode(encryptor.update(x.encode())).decode())

        encrypted_data = df.to_csv(index=False)
        return encrypted_data

    def decrypt_data(self, encrypted_data, schema_info, dek_id, kek_id):
        """
        Decrypt specific columns in the given data based on schema info
        """
        dek = self._get_dek(dek_id, kek_id)

        # Load the encrypted data as a DataFrame
        data_io = BytesIO(encrypted_data.encode())
        df = pd.read_csv(data_io)

        # Identify columns to decrypt based on schema info
        columns_to_encrypt = [schema['Column Name'] for schema in schema_info if schema.get("PII", "Y") == "Y" or schema.get("Masking Required", "N") == "Y"]

        # Decrypt specified columns
        cipher = Cipher(algorithms.AES(dek), modes.CFB(BLOCK_SIZE * b'\x00'), backend=default_backend())
        decryptor = cipher.decryptor()

        for column in columns_to_encrypt:
            df[column] = df[column].apply(lambda x: decryptor.update(base64.b64decode(x.encode())).decode())

        decrypted_data = df.to_csv(index=False)
        return decrypted_data
