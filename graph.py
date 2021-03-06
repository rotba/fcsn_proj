import math
import itertools
import random
from functools import reduce

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

    def parse_edge(self, edge):
        numbers_series = edge.split(',')
        return Edge.create(numbers_series[0], numbers_series[1], numbers_series[2:])

    def add_edge(self, parsed_edge):
        self._edges.append(parsed_edge)
        self.add_two_way_edge(parsed_edge._u, parsed_edge._v, parsed_edge.get_weight())

    def print_graph(self):
        print ('Num_Nodes = {}'.format(self.get_num_of_nodes()))
        print ('initial node = {}'.format(self.get_initial_node()))
        print ('end node = {}'.format(self.get_dest_node()))
        print ('========== EDGES ==========')
        for edge in self._edges:
            print (edge.to_string())

    @staticmethod
    def calc_factors(parsed_edges):
        def calc_factor(i_weights):
            the_sum = sum(i_weights)
            return math.ceil(math.log(the_sum, 2))

        ans = []
        if len(parsed_edges) == 0:
            return []
        for i in range(len(parsed_edges[0]._weights)):
            ans += [calc_factor(map(lambda e: e._weights[i], parsed_edges))]
        return ans

    @staticmethod
    def edges_for_random_graph(num_nodes, density_factor=0.4, weight_max=7):
        # graph declaration
        edges = []
        for i,j in itertools.combinations(range(num_nodes), 2):
            rnd = random.uniform(0, 1)
            if rnd < density_factor:
                edges += [Edge.create(i, j, [random.randrange(1, weight_max), random.randrange(1, weight_max),
                                     random.randrange(1, weight_max)])]
        return edges

    @staticmethod
    def from_text(file_path):
        with open(file_path, "r") as input_file:
            input_iter = input_file.__iter__()
            num_of_nodes = int(next(input_iter))
            k = int(next(input_iter))
            initial_node_number = int(next(input_iter))
            dest_node_number = int(next(input_iter))

            # graph declaration
            graph = Graph()
            for i in range(num_of_nodes):
                graph.add_node(i)

            edgestr = next(input_iter)

            pared_edges = []
            if edgestr.strip().lower() == 'r':
                density = next(input_iter, None)
                try:
                    density = float(density)
                    pared_edges = Graph.edges_for_random_graph(num_of_nodes, density_factor=density)
                except TypeError:
                    pared_edges = Graph.edges_for_random_graph(num_of_nodes)
            else:
                pared_edges += [graph.parse_edge(edgestr)]
                for edge in input_iter:
                    pared_edges += [graph.parse_edge(edge)]

            factors = Graph.calc_factors(pared_edges)
            for edge in pared_edges:
                edge.set_factors(factors)
                graph.add_edge(edge)
            graph.set_num_of_nodes(num_of_nodes)
            graph.set_initial_node(initial_node_number)
            graph.set_dest_node(dest_node_number)
            graph.set_dest_k(k)
            return graph

    def copy_and_return(self):
        ret_g = Graph()
        ret_g.num_nodes = self.num_nodes
        ret_g.set_initial_node(self._initial_node)
        ret_g.set_dest_node(self._dest_node)
        ret_g.set_num_of_nodes(self._num_of_nodes)
        ret_g.set_dest_k(self._k)
        for i in range(ret_g._num_of_nodes):
            ret_g.add_node(i)
        for edge in self._edges:
            ret_g.add_edge(edge.copy_and_return())
        return ret_g

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
        def check_all_edges_contained(g1, g2):
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
        return Edge(u, v, weights)

    def __init__(self, u, v, weights):
        self._u = int(u)
        self._v = int(v)
        self._weights = list(map(int, weights))
        self._factors = [1] * len(weights)

    def get_tuple(self):
        return (self._u, self._v)

    def get_tuple_rev(self):
        return ( self._v ,self._u)

    def to_string(self):
        return '{},{},{},{}'.format(self._u, self._v, self._weights,self.get_weight())

    def copy_and_return(self):
        ret_e = Edge(self._u, self._v, self._weights)
        ret_e.set_factors(self._factors)
        return ret_e

    def set_factors(self, factors):
        self._factors = factors

    def get_weight(self):
        if len(self._weights) == 0:
            return 0;
        shifts = list(reversed(
            reduce(
                lambda acc, curr: acc + [acc[-1] + curr],
                reversed(self._factors[1:]),
                [0]
            )
        ))
        return reduce(
            lambda acc, curr: curr[0] * math.pow(2, curr[1]) + acc,
            zip(self._weights, shifts),
            0
        )
