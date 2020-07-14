import re
import ast

class Solution(object):

	def __init__(self):
		self._paths = {}

	def add_path(self, index, path, total_weight):
		self._paths[index] = Path(path, total_weight)

	def __eq__(self, other):
		if not len(other._paths) == len(self._paths):
			return False

		for k in other._paths.keys():
			if not self._paths[k] == other._paths[k]:
				return False

		for k in self._paths.keys():
			if not self._paths[k] == other._paths[k]:
				return False
		return True

	@staticmethod
	def from_txt(file_path):
		def extract_index(line):
			return int(re.findall("^(Shortest Path )(\d+)", line)[0][1])

		def extract_path(line):
			return map(int,line.strip(str(re.findall("^(Shortest Path )(\d+)", line)[0])).strip(':').strip('\n').strip(' [').strip(']').split(','))

		def extract_totalweigth(line):
			return int(re.findall("^(Path Total Weight: )(\d+)", line)[0][1])

		solution = Solution()
		file_iter = open(file_path, "r").__iter__()
		for line in file_iter:
			solution.add_path(
				extract_index(line),
				extract_path(line),
				extract_totalweigth(file_iter.next()),
			)
		return solution


class Path(object):
	def __init__(self, path, total_weight):
		self._path = path
		self._total_weight =total_weight

	def __eq__(self, other):
		return self._path == other._path and self._total_weight == other._total_weight