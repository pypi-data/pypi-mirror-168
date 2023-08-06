from abc import ABC, abstractmethod


class BaseDecryptionProvider(ABC):
    """
    Provides a way to decrypt encrypted messages.

    Various implementations might use AWS KMS, Azure, etc.
    """

    @abstractmethod
    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt secrets.

        Receives encrypted cipher text and returns the decrypted plain text.
        """
        pass
