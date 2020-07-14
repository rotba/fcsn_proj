import unittest

from main import solve
from solution import Solution

in_0 = "in_0.txt"
exp_out_0 = "exp_out_0.txt"

class MyTestCase(unittest.TestCase):
	def test_0(self):
		self.assertEqual(solve(in_0), Solution.from_txt(exp_out_0))


if __name__ == '__main__':
	unittest.main()
