from mnemonic import Mnemonic
import hashlib
import base64
from cryptography.fernet import Fernet

class SeedHandler:
    def __init__(self):
        self.mnemo = Mnemonic("english")

    def generate_seed_phrase(self) -> str:
        return self.mnemo.generate(strength=128)

    def seed_to_key(self, seed_phrase: str) -> bytes:
        seed = self.mnemo.to_seed(seed_phrase)
        raw_key = hashlib.sha256(seed).digest()
        private_key = base64.urlsafe_b64encode(raw_key)
        return private_key

    def get_public_key(self, private_key: bytes) -> str:
        return hashlib.sha256(private_key).hexdigest()

    def get_fernet(self, private_key: bytes) -> Fernet:
        return Fernet(Fernet.generate_key_from_password(private_key))

