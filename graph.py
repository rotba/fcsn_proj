from node import *


class Graph:
	def __init__(self):
		self.dict_nodes = {}
		self._edges = []
		self.num_nodes = 0

	def add_node(self, number):
		self.num_nodes = self.num_nodes + 1
		cur_node = Node(number)
		self.dict_nodes[number] = cur_node

		return cur_node

	def add_two_way_edge(self, node_a, node_b, weight=0):
		self.dict_nodes[node_a].add_edge(self.dict_nodes[node_b], weight)
		self.dict_nodes[node_b].add_edge(self.dict_nodes[node_a], weight)

	def delete_minor_edge(self, minimumPathList):
		initial_node = {}
		final_node = {}
		final_weight = main.INFINITY

		# finds the lightest edge between the edges related to the shortest path elements
		for x in minimumPathList:
			for y in self.dict_nodes[x].neighbor_with_weights:
				weight = self.dict_nodes[x].neighbor_with_weights[y]
				if (final_weight > weight) and (exitst_in_minimum_path(minimumPathList, y.number)):
					final_weight = weight
					initial_node = x
					final_node = y.number

		# erases the path of the lower weight edge from the graph
		if final_node != {}:
			for j in self.dict_nodes[initial_node].neighbor_with_weights:
				if j.number == final_node:
					self.dict_nodes[initial_node].neighbor_with_weights.pop(j)
					break
			for i in self.dict_nodes[final_node].neighbor_with_weights:
				if i.number == initial_node:
					self.dict_nodes[final_node].neighbor_with_weights.pop(i)
					break

	def __iter__(self):
		return iter(self.dict_nodes.values())

	def parse_edge(self, edge, g_reduce = False):
		numbers_series = edge.split(',')
		return Edge.create(numbers_series[0], numbers_series[1], numbers_series[2:], g_reduce=g_reduce)

	def add_edge(self, parsed_edge):
		self.add_two_way_edge(parsed_edge._u, parsed_edge._v, parsed_edge.get_weight())

	@staticmethod
	def from_text(file_path, g_reduce=False):
		input_file = open(file_path, "r")
		input_iter = input_file.__iter__()
		num_of_nodes = int(input_iter.next())
		k = int(input_iter.next())
		initial_node_number = int(input_iter.next())
		dest_node_number = int(input_iter.next())

		# graph declaration
		graph = Graph()
		for i in range(num_of_nodes):
			graph.add_node(i)

		for edge in input_iter:
			parsed_edge = graph.parse_edge(edge,g_reduce=g_reduce)
			graph.add_edge(parsed_edge)
		graph.set_num_of_nodes(num_of_nodes)
		graph.set_initial_node(initial_node_number)
		graph.set_dest_node(dest_node_number)
		graph.set_dest_k(k)

		return graph

	def set_initial_node(self, initial_node_number):
		self._initial_node = initial_node_number

	def set_dest_node(self, dest_node_number):
		self._dest_node = dest_node_number

	def set_dest_k(self, k):
		self._k = k

	def get_initial_node(self):
		return self._initial_node

	def get_dest_node(self):
		return self._dest_node

	def get_num_of_nodes(self):
		return self._num_of_nodes

	def set_num_of_nodes(self, num_of_nodes):
		self._num_of_nodes = num_of_nodes

	def get_k(self):
		return self._k

	def __eq__(self, other):
		def check_all_edges_contained(g1,g2):
			for u1 in g1.dict_nodes.keys():
				node_u1 = g1.dict_nodes[u1]
				node_u2 = other.dict_nodes[u1]
				for neighbor in node_u1.get_neighbors():
					if not neighbor.number in map(lambda x: x.number, node_u2.get_neighbors()):
						return False
					if not node_u1.get_weight(neighbor) == node_u2.get_weight(g2.dict_nodes[neighbor.number]):
						return False
			return True

		if self._num_of_nodes != other._num_of_nodes:
			return False

		if not (check_all_edges_contained(self, other) or check_all_edges_contained(other, self)):
			return False
		return True


def exitst_in_minimum_path(minimumPathList, a):
	if a in minimumPathList:
		return True
	else:
		return False


class Edge(object):

	@staticmethod
	def create(u, v, weights, g_reduce=False):
		if g_reduce:
			return ReducedEdge(u, v, weights)
		else:
			return Edge(u, v, weights)

	def __init__(self, u, v, weights):
		self._u = int(u)
		self._v = int(v)
		self._weights = map(int, weights)

	def get_weight(self):
		return reduce(
			lambda curr, acc: curr + acc,
			self._weights,
			0
		)


class ReducedEdge(Edge):
	def get_weight(self):
		return reduce(
			lambda curr, acc: curr + acc,
			self._weights,
			0
		)
