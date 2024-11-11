import time
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
from lab3 import RC5CBCPad


class RSAEncryption:
    def __init__(self, key_size=2048):
        if key_size < 2048:
            raise ValueError("Key size must be at least 2048 bits for security purposes.")
        self.key_size = key_size
        self.private_key = None
        self.public_key = None


    def generate_keys(self):
        key = RSA.generate(self.key_size)
        self.private_key = key
        self.public_key = key.publickey()

    def save_keys(self, private_key_path, public_key_path):
        with open(private_key_path, 'wb') as priv_file:
            priv_file.write(self.private_key.export_key())
        with open(public_key_path, 'wb') as pub_file:
            pub_file.write(self.public_key.export_key())

    def load_private_key(self, path):
        with open(path, 'rb') as priv_file:
            self.private_key = RSA.import_key(priv_file.read())

    def load_public_key(self, path):
        with open(path, 'rb') as pub_file:
            self.public_key = RSA.import_key(pub_file.read())

    def encrypt(self, plaintext):
        symmetric_key = get_random_bytes(16)

        cipher_aes = AES.new(symmetric_key, AES.MODE_GCM)
        ciphertext, tag = cipher_aes.encrypt_and_digest(plaintext)

        cipher_rsa = PKCS1_OAEP.new(self.public_key)
        encrypted_symmetric_key = cipher_rsa.encrypt(symmetric_key)

        return encrypted_symmetric_key + cipher_aes.nonce + tag + ciphertext

    def decrypt(self, ciphertext):
        encrypted_symmetric_key = ciphertext[:self.private_key.size_in_bytes()]
        nonce = ciphertext[self.private_key.size_in_bytes():self.private_key.size_in_bytes() + 16]
        tag = ciphertext[self.private_key.size_in_bytes() + 16:self.private_key.size_in_bytes() + 32]
        ciphertext = ciphertext[self.private_key.size_in_bytes() + 32:]

        cipher_rsa = PKCS1_OAEP.new(self.private_key)
        symmetric_key = cipher_rsa.decrypt(encrypted_symmetric_key)

        cipher_aes = AES.new(symmetric_key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher_aes.decrypt_and_verify(ciphertext, tag)

        return plaintext

    def test_rsa_vs_rc5(self, file_path, rc5_key=b'secret_key_16b'):
        rc5 = RC5CBCPad(rc5_key)

        with open(file_path, 'rb') as file:
            data = file.read()

        start_time = time.time()
        encrypted_rsa = self.encrypt(data)
        rsa_encrypt_time = time.time() - start_time

        start_time = time.time()
        decrypted_rsa = self.decrypt(encrypted_rsa)
        rsa_decrypt_time = time.time() - start_time

        assert decrypted_rsa == data, "RSA дешифрування не відтворює початкові дані!"


        iv = os.urandom(rc5.block_size)
        start_time = time.time()
        encrypted_rc5 = rc5.encrypt_console(data, iv)
        rc5_encrypt_time = time.time() - start_time

        start_time = time.time()
        decrypted_rc5 = rc5.decrypt_console(encrypted_rc5, iv)
        rc5_decrypt_time = time.time() - start_time

        assert decrypted_rc5 == data, "RC5 дешифрування не відтворює початкові дані!"

        comparison = {
            "RSA Encryption Time": rsa_encrypt_time,
            "RSA Decryption Time": rsa_decrypt_time,
            "RC5 Encryption Time": rc5_encrypt_time,
            "RC5 Decryption Time": rc5_decrypt_time,
            "RSA faster in Encryption": rsa_encrypt_time < rc5_encrypt_time,
            "RSA faster in Decryption": rsa_decrypt_time < rc5_decrypt_time,
        }
        return comparison