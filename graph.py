import main
from node import *


class Graph:
    def __init__(self):
        self.dict_nodes = {}
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

        #finds the lightest edge between the edges related to the shortest path elements
        for x in minimumPathList:
            for y in self.dict_nodes[x].neighbor_with_weights:
                weight = self.dict_nodes[x].neighbor_with_weights[y]
                if(final_weight > weight) and (exitst_in_minimum_path(minimumPathList, y.number)):
                    final_weight = weight
                    initial_node = x
                    final_node = y.number


        #erases the path of the lower weight edge from the graph
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
        return Edge(numbers_series[0], numbers_series[1], numbers_series[2:])

    def add_edge(self, parsed_edge):
        self.add_two_way_edge(parsed_edge._u, parsed_edge._v, parsed_edge.get_weight())


def exitst_in_minimum_path(minimumPathList, a):
    if a in minimumPathList:
        return True
    else:
        return False


class Edge(object):

    def __init__(self, u, v, weights):
        self._u = int(u)
        self._v = int(v)
        self._weights = map(int, weights)

    def get_weight(self):
        return reduce(
            lambda curr, acc: curr+acc,
            self._weights,
            0
        )