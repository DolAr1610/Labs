import unittest
import os
import time
from Crypto.Random import get_random_bytes
from business.lab4 import RSAEncryption
from business.lab3 import RC5CBCPad


class TestRSAEncryption(unittest.TestCase):
    def setUp(self):
        self.rsa_encryption = RSAEncryption(key_size=2048)
        self.rsa_encryption.generate_keys()

        self.private_key_path = "private_test.pem"
        self.public_key_path = "public_test.pem"

        self.rc5_key = b'secret_key_16b'
        self.rc5 = RC5CBCPad(self.rc5_key)

    def tearDown(self):
        if os.path.exists(self.private_key_path):
            os.remove(self.private_key_path)
        if os.path.exists(self.public_key_path):
            os.remove(self.public_key_path)

    def test_generate_keys(self):
        self.assertIsNotNone(self.rsa_encryption.private_key)
        self.assertIsNotNone(self.rsa_encryption.public_key)
        self.assertEqual(self.rsa_encryption.private_key.size_in_bits(), 2048)

    def test_save_and_load_keys(self):
        self.rsa_encryption.save_keys(self.private_key_path, self.public_key_path)
        rsa_new_instance = RSAEncryption()
        rsa_new_instance.load_private_key(self.private_key_path)
        rsa_new_instance.load_public_key(self.public_key_path)

        self.assertEqual(self.rsa_encryption.private_key.export_key(), rsa_new_instance.private_key.export_key())
        self.assertEqual(self.rsa_encryption.public_key.export_key(), rsa_new_instance.public_key.export_key())

    def test_rsa_encryption_decryption(self):
        plaintext = b"Test message for encryption"
        encrypted_data = self.rsa_encryption.encrypt(plaintext)
        decrypted_data = self.rsa_encryption.decrypt(encrypted_data)

        self.assertEqual(plaintext, decrypted_data)

    def test_rc5_encryption_decryption(self):
        plaintext = b"Test message for RC5 encryption"
        iv = os.urandom(self.rc5.block_size)
        encrypted_data = self.rc5.encrypt_console(plaintext, iv)
        decrypted_data = self.rc5.decrypt_console(encrypted_data, iv)

        self.assertEqual(plaintext, decrypted_data)

    def test_rsa_vs_rc5(self):
        test_data = get_random_bytes(1024)

        rsa_start_time = time.time()
        encrypted_rsa = self.rsa_encryption.encrypt(test_data)
        rsa_encrypt_time = time.time() - rsa_start_time

        rsa_start_time = time.time()
        decrypted_rsa = self.rsa_encryption.decrypt(encrypted_rsa)
        rsa_decrypt_time = time.time() - rsa_start_time

        self.assertEqual(decrypted_rsa, test_data)

        iv = os.urandom(self.rc5.block_size)
        rc5_start_time = time.time()
        encrypted_rc5 = self.rc5.encrypt_console(test_data, iv)
        rc5_encrypt_time = time.time() - rc5_start_time

        rc5_start_time = time.time()
        decrypted_rc5 = self.rc5.decrypt_console(encrypted_rc5, iv)
        rc5_decrypt_time = time.time() - rc5_start_time

        self.assertEqual(decrypted_rc5, test_data)

        print(f"RSA Encryption Time: {rsa_encrypt_time:.6f} seconds")
        print(f"RSA Decryption Time: {rsa_decrypt_time:.6f} seconds")
        print(f"RC5 Encryption Time: {rc5_encrypt_time:.6f} seconds")
        print(f"RC5 Decryption Time: {rc5_decrypt_time:.6f} seconds")

        self.assertTrue(rsa_encrypt_time < rc5_encrypt_time or rc5_encrypt_time < rsa_encrypt_time)
        self.assertTrue(rsa_decrypt_time < rc5_decrypt_time or rc5_decrypt_time < rsa_decrypt_time)


if __name__ == "__main__":
    unittest.main()
