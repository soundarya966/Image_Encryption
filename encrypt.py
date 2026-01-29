import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

password = input("Enter secret key: ").encode()

with open("images/sample.jpg", "rb") as f:
    data = f.read()

salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
)
key = kdf.derive(password)

iv = os.urandom(16)
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
encryptor = cipher.encryptor()

padder = padding.PKCS7(128).padder()
padded_data = padder.update(data) + padder.finalize()

encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

with open("encrypted/sample.enc", "wb") as f:
    f.write(salt + iv + encrypted_data)

print("Image encrypted successfully")
