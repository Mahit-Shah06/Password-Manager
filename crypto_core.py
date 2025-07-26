from cryptography.fernet import Fernet

class Encrypter:

    def __init__(self, key: bytes = None):
        if key is None:
            raise ValueError("Encryption key must be derived from seed. None provided.")

        self.key = key
        self.fernet = Fernet(self.key)
    
    def encryption(self, data: str) -> str:
        encrypted_data = self.fernet.encrypt(data.encode('utf-8'))
        return encrypted_data.decode('utf-8')

    def decryption(self, token: str) -> str:
        encrypted_data = token.encode('utf-8')
        return self.fernet.decrypt(encrypted_data).decode('utf-8')

    def get_key(self) -> bytes:
        return self.key