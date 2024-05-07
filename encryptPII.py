import logging
import json
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from pymongo import MongoClient, errors as mongo_errors
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Custom exception class for application-specific errors
class DataEncryptionError(Exception):
    pass

def encrypt_sensitive_data(data_bytes, client_id, client_secret, tenant_id, key_vault_name, mongo_connection_str, db_name, schema_collection, table_name):
    try:
        # Authenticate with Azure Key Vault using client ID, client secret, and tenant ID
        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
        )

        # Connect to Azure Key Vault
        key_vault_url = f"https://{key_vault_name}.vault.azure.net/"
        key_vault_client = SecretClient(vault_url=key_vault_url, credential=credential)

        # Retrieve secrets from Azure Key Vault
        try:
            master_key = key_vault_client.get_secret("your_master_key_secret_name").value
            encrypted_kek = key_vault_client.get_secret("your_kek_secret_name").value
            encrypted_dek = key_vault_client.get_secret("your_dek_secret_name").value
        except Exception as e:
            raise DataEncryptionError(f"Failed to retrieve secrets from Key Vault: {e}")

        # Decrypt KEK with the Master Key
        try:
            master_key_suite = Fernet(master_key)
            kek = master_key_suite.decrypt(encrypted_kek.encode())
        except InvalidToken:
            raise DataEncryptionError("Invalid Master Key or KEK decryption failed.")

        # Decrypt DEK with the KEK
        try:
            kek_suite = Fernet(kek)
            dek = kek_suite.decrypt(encrypted_dek.encode())
        except InvalidToken:
            raise DataEncryptionError("Invalid KEK or DEK decryption failed.")

        # Connect to MongoDB to retrieve schema information for the specified table
        try:
            mongo_client = MongoClient(mongo_connection_str)
            schema_collection = mongo_client[db_name][schema_collection]
        except mongo_errors.PyMongoError as e:
            raise DataEncryptionError(f"Failed to connect to MongoDB: {e}")

        # Retrieve schema for the given table
        try:
            schema_docs = schema_collection.find({"Table Name": table_name})
        except Exception as e:
            raise DataEncryptionError(f"Failed to retrieve schema from MongoDB: {e}")

        # Identify columns to encrypt based on schema
        try:
            columns_to_encrypt = [doc["Column Name"] for doc in schema_docs if doc.get("PII") == "Y" or doc.get("encryption") == "Y"]
        except Exception as e:
            raise DataEncryptionError(f"Failed to identify columns to encrypt: {e}")

        # Encrypt sensitive columns using the DEK
        try:
            dek_suite = Fernet(dek)
            data_dict = json.loads(data_bytes)  # Convert bytes to dictionary
            for column in columns_to_encrypt:
                if column in data_dict:
                    encrypted_value = dek_suite.encrypt(data_dict[column].encode()).decode()  # Convert to bytes, then decode
                    data_dict[column] = encrypted_value
            encrypted_data_bytes = json.dumps(data_dict).encode()  # Convert back to bytes
        except Exception as e:
            raise DataEncryptionError(f"Error encrypting data: {e}")

        # Return the encrypted data
        return encrypted_data_bytes
    
    except DataEncryptionError as e:
        logging.error(f"Data encryption error: {e}")
        raise  # Raise to notify the calling function/module

    except Exception as e:
        logging.error(f"Unexpected error in encrypt_sensitive_data: {e}")
        raise  # Raise to propagate unexpected errors

# Example of calling the function
if __name__ == "__main__":
    data_bytes = b'{"ColumnName1": "SensitiveData", "ColumnName2": "PublicData"}'
    client_id = "your_client_id"
    client_secret = "your_client_secret"
    tenant_id = "your_tenant_id"
    key_vault_name = "your_key_vault_name"
    mongo_connection_str = "your_mongo_connection_string"
    db_name = "your_db_name"
    schema_collection = "your_schema_collection"
    table_name = "your_table_name"

    try:
        # Call the function to encrypt sensitive data
        encrypted_data = encrypt_sensitive_data(
            data_bytes,
            client_id,
            client_secret,
            tenant_id,
            key_vault_name,
            mongo_connection_str,
            db_name,
            schema_collection,
            table_name,
        )
        logging.info(f"Encrypted data: {encrypted_data}")

    except Exception as e:
        logging.error(f"Error occurred: {e}")
