import unittest
from business.lab1 import LemerGenerator, gcd, estimate_pi

class TestLemerGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = LemerGenerator(seed=11, a=48271, c=0, m=2**31)

    def test_next_generation(self):
        number = self.gen.next()
        self.assertIsInstance(number, int)
        self.assertEqual(len(self.gen.generated_numbers), 1)

    def test_get_bytes(self):
        bytes_data = self.gen.get_bytes(16)
        self.assertEqual(len(bytes_data), 16)

    def test_save_to_file(self):
        self.gen.next()
        self.gen.save_to_file("test_output.txt")
        with open("test_output.txt", "r") as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 1)

    def test_find_period(self):
        for _ in range(100):
            self.gen.next()
        period = self.gen.find_period()
        self.assertGreaterEqual(period, 1)

class TestMathFunctions(unittest.TestCase):
    def test_gcd(self):
        self.assertEqual(gcd(54, 24), 6)
        self.assertEqual(gcd(101, 10), 1)

    def test_estimate_pi(self):
        estimate = estimate_pi(1000, lambda: 42)
        self.assertIsInstance(estimate, float)

if __name__ == "__main__":
    unittest.main()
