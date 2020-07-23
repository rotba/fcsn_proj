import main
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

class Dijkstra:
    priorityQ = Q.PriorityQueue()
    dict_distance_to_initial_node = {}
    last_node_table = {}
    minimunPathList = []

    def __init__(self, graph, initial_node, final_node):
        self.minimunPathList = []
        for x in graph.dict_nodes:
            self.dict_distance_to_initial_node[x] = main.INFINITY
            self.last_node_table[x] = initial_node

        self.priorityQ.put((0, initial_node))
        self.dict_distance_to_initial_node[initial_node] = 0

        while not self.priorityQ.empty():
            source_node_name = self.priorityQ.get()[1]
            for dest_node in graph.dict_nodes[source_node_name].get_neighbors():
                addition = graph.dict_nodes[source_node_name].get_weight(dest_node)
                new_distance = self.dict_distance_to_initial_node[source_node_name] + addition
                dest_node_name = dest_node.get_number()
                if (new_distance < self.dict_distance_to_initial_node[dest_node_name]):
                    self.dict_distance_to_initial_node[dest_node_name] = new_distance
                    self.priorityQ.put((new_distance, dest_node_name))
                    self.last_node_table[dest_node_name] = source_node_name

        # builds list forming the shortest path from the final node through the previous table
        # until you reach the start node
        self.minimunPathList.append(final_node)
        previous_node = self.last_node_table[final_node]
        while initial_node != previous_node:
            self.minimunPathList.append(previous_node)
            previous_node = self.last_node_table[previous_node]
        self.minimunPathList.append(initial_node)
        self.minimunPathList = list(reversed(self.minimunPathList))
