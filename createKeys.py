import base64
import logging
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.padding import OAEP
from cryptography.hazmat.primitives.asymmetric import keywrap
from cryptography.hazmat.primitives.ciphers import Cipher, modes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Azure Key Vault credentials and settings
KV_URL = "<your-key-vault-url>"
CLIENT_ID = "<your-client-id>"
CLIENT_SECRET = "<your-client-secret>"
TENANT_ID = "<your-tenant-id>"

# Create Azure Key Vault client
credential = ClientSecretCredential(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, tenant_id=TENANT_ID)
client = SecretClient(vault_url=KV_URL, credential=credential)

# Create KEK (RSA 4096)
kek = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
    backend=default_backend(),
)

# Export KEK public key and private key in PEM format
kek_public_pem = kek.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)
kek_private_pem = kek.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)

# Store KEK public key and private key in Azure Key Vault as secrets
kek_pub_id = "kek_id_rsa_pub"
kek_priv_id = "kek_id_rsa"

client.set_secret(kek_pub_id, base64.b64encode(kek_public_pem).decode())
client.set_secret(kek_priv_id, base64.b64encode(kek_private_pem).decode())

logger.info(f"Stored KEK public and private keys in Azure Key Vault with IDs: {kek_pub_id}, {kek_priv_id}")

# Create DEK (AES 256)
dek = algorithms.AES.generate_key(256)  # AES-256 key

# Wrap the DEK with the KEK (Key Wrapping)
wrapped_dek = kek.public_key().encrypt(
    dek,
    OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)

# Store the wrapped DEK in Azure Key Vault
dek_id = "dek_id"

client.set_secret(dek_id, base64.b64encode(wrapped_dek).decode())

logger.info(f"Stored DEK in Azure Key Vault with ID: {dek_id}")
