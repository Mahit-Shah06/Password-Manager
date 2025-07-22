from cryptography.fernet import Fernet
import os

class Encrypter:

    KEY_FILE = "secret.key" 

    def __init__(self, key: bytes = None):
        if key:
            self.key = key
        elif os.path.exists(self.KEY_FILE):
            with open(self.KEY_FILE, 'rb') as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(self.KEY_FILE, 'wb') as f:
                f.write(self.key)

        self.fernet = Fernet(self.key)
    
    def encryption(self, data: str) -> str:
        encrypted_data = self.fernet.encrypt(data.encode('utf-8'))
        return encrypted_data.decode('utf-8')

    def decryption(self, token: str) -> str:
        print(f"Trying to decrypt token: {token}")
        encrypted_data = token.encode('utf-8')
        return self.fernet.decrypt(encrypted_data).decode('utf-8')

    def get_key(self) -> bytes:
        return self.key