import main


class Node:
    def __init__(self, number):
        self.number = number
        self.neighbor_with_weights = {}
        self.distance = main.INFINITY

    def add_edge(self, neighbor, weight=0):
        self.neighbor_with_weights[neighbor] = weight

    def remove_edge(self, neighbor):
        self.neighbor_with_weights.pop(neighbor)

    def set_distance(self, distance):
        self.distance = distance

    def get_neighbors(self):
        return self.neighbor_with_weights.keys()

    def get_number(self):
        return self.number

    def get_weight(self, neighbor):
        return self.neighbor_with_weights[neighbor]

    def get_distance(self):
        return self.distance
