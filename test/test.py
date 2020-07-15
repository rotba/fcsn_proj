import unittest

from main import solve, Graph
from solution import Solution

in_0 = "alg/in_0.txt"
exp_out_0 = "alg/exp_out_0.txt"

red_in_0 = "reduction/in_0.txt"
red_exp_out_0 = "reduction/exp_out_0.txt"

class MyTestCase(unittest.TestCase):

	# def test_0(self):
	# 	self.assertEqual(solve(in_0), Solution.from_txt(exp_out_0))

	def test_reduction(self):
		self.assertEqual(Graph.from_text(red_in_0), Graph.from_text(red_exp_out_0))


if __name__ == '__main__':
	unittest.main()
