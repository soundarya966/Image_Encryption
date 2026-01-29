from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

password = input("Enter secret key: ").encode()

with open("encrypted/sample.enc", "rb") as f:
    file_data = f.read()

salt = file_data[:16]
iv = file_data[16:32]
encrypted_data = file_data[32:]

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
)
key = kdf.derive(password)

cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
decryptor = cipher.decryptor()

padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

unpadder = padding.PKCS7(128).unpadder()
data = unpadder.update(padded_data) + unpadder.finalize()

with open("decrypted/sample.jpg", "wb") as f:
    f.write(data)

print("Image decrypted successfully")
