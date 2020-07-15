import sys
from graph import *
from djikstra import *
from solution import Solution

INFINITY = 999999999

def solve(input):
    solution = Solution()
    infinity = INFINITY
    input_file = open(input, "r")
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
        parsed_edge = graph.parse_edge(edge)
        graph.add_edge(parsed_edge)

    if initial_node_number > 0 and dest_node_number <= num_of_nodes:
        u = 0
        pathToSelf = False
        while u < k:
            if dest_node_number in graph.dict_nodes:
                dijkstra = Dijkstra(graph, graph.dict_nodes[initial_node_number].get_number(),
									graph.dict_nodes[dest_node_number].get_number())
                if dijkstra.dict_distance_to_initial_node[dest_node_number] < infinity and pathToSelf == False:
                    print "Shortest Path " + str(u + 1) + ": " + str(dijkstra.minimunPathList)
                    print "Path Total Weight: " + str(dijkstra.dict_distance_to_initial_node[dest_node_number])
                    solution.add_path(u + 1, dijkstra.minimunPathList,
									  dijkstra.dict_distance_to_initial_node[dest_node_number])
                    graph.delete_minor_edge(dijkstra.minimunPathList)
                    if dijkstra.dict_distance_to_initial_node[dest_node_number] == 0:
                        pathToSelf = True
                else:
                    u = k
                    print "All Possible Paths Found"
            u = u + 1
    else:
        print "arguments 2 and 3 must be btween 1 and num of nodes"

    return solution


def main():
    sol = solve(
        sys.argv[1]
    )


if __name__ == '__main__':
    main()
