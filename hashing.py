import hashlib
import pygame

pygame.init()

# Police de caractères
small_font = pygame.font.Font(None, 24)

class CryptographicHash:
    def __init__(self):
        pass

    def md5_hash(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    def sha256_hash(self, text):
        return hashlib.sha256(text.encode()).hexdigest()

class ExtendableHashing:
    def __init__(self):
        pass

    # Implement Extendable Hashing logic here
    pass


