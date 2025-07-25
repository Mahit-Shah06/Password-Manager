from mnemonic import Mnemonic
import hashlib
from cryptography.fernet import Fernet

class SeedHandler:
    def __init__(self):
        self.mnemo = Mnemonic("english")

    def generate_seed_phrase(self) -> str:
        return self.mnemo.generate(strength=128)

    def seed_to_key(self, seed_phrase: str) -> bytes:
        seed = self.mnemo.to_seed(seed_phrase)
        return hashlib.sha256(seed).digest()

    def get_public_key(self, private_key: bytes) -> str:
        return hashlib.sha256(private_key).hexdigest()

    def get_fernet(self, private_key: bytes) -> Fernet:
        return Fernet(Fernet.generate_key_from_password(private_key))

