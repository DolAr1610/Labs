import unittest
from lab3 import RC5CBCPad

class TestRC5CBCPad(unittest.TestCase):
    def setUp(self):
        self.rc5 = RC5CBCPad(key=b"secret_key")

    def test_pad_key(self):
        padded_key = self.rc5._pad_key(b"short_key", 16)
        self.assertEqual(len(padded_key), 16)

    def test_xor_bytes(self):
        result = self.rc5._xor_bytes(b"\x01\x02", b"\x03\x04")
        self.assertEqual(result, b"\x02\x06")

    def test_pad_data(self):
        padded_data = self.rc5._pad_data(b"test")
        self.assertEqual(len(padded_data) % self.rc5.block_size, 0)

    def test_unpad_data(self):
        padded_data = self.rc5._pad_data(b"test")
        unpadded_data = self.rc5._unpad_data(padded_data)
        self.assertEqual(unpadded_data, b"test")

    def test_encrypt_decrypt(self):
        data = b"hello world!!"
        padded_data = self.rc5._pad_data(data)
        encrypted_blocks = [self.rc5._rc5_encrypt_block(block) for block in self.rc5._split_blocks(padded_data)]
        decrypted_blocks = [self.rc5._rc5_decrypt_block(block) for block in encrypted_blocks]
        decrypted_data = self.rc5._unpad_data(b"".join(decrypted_blocks))
        self.assertEqual(decrypted_data, data)

if __name__ == "__main__":
    unittest.main()
