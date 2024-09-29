from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

class SecretProvider:
    _client = None

    @classmethod
    def _get_client(cls):
        if cls._client is None:
            key_vault_url = "https://your-keyvault-name.vault.azure.net/"
            credential = DefaultAzureCredential()
            cls._client = SecretClient(vault_url=key_vault_url, credential=credential)
        return cls._client

    @classmethod
    def get_secret(cls, secret_name):
        client = cls._get_client()
        return client.get_secret(secret_name).value