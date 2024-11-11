import unittest
from lab2 import MD5, md5_string, md5_file, verify_file

class TestMD5(unittest.TestCase):
    def test_md5_hashing(self):
        md5 = MD5()
        md5.update(b"test")
        self.assertEqual(len(md5.hexdigest()), 32)

    def test_md5_string(self):
        hash_result = md5_string("test")
        self.assertEqual(len(hash_result), 32)
        self.assertIsInstance(hash_result, str)

    def test_md5_file(self):
        with open("test_file.txt", "wb") as f:
            f.write(b"test")
        hash_result = md5_file("test_file.txt")
        self.assertEqual(len(hash_result), 32)

    def test_verify_file(self):
        with open("test_file.txt", "wb") as f:
            f.write(b"test")
        expected_hash = md5_file("test_file.txt")
        self.assertTrue(verify_file("test_file.txt", expected_hash))

if __name__ == "__main__":
    unittest.main()
