import sys
import networkx as nx
import matplotlib.pyplot as plt
try:
    import pygraphviz
    from networkx.drawing.nx_agraph import write_dot
    print("using package pygraphviz")
except ImportError:
    try:
        import pydot
        from networkx.drawing.nx_pydot import write_dot
        print("using package pydot")
    except ImportError:
        print()
        print("Both pygraphviz and pydot were not found ")
        print("see  https://networkx.github.io/documentation/latest/reference/drawing.html")
        print()
        raise

from djikstra import *
from graph import *
from solution import Solution


INFINITY = 999999999


def plot_graph_and_sol(graph_copy, solution):
	G = nx.Graph()
	for edge in graph_copy._edges:
		G.add_edge(edge._u,edge._v, label='{}={}'.format(edge._weights, edge.get_weight()))
	edge_path_shortest = []
	if len(solution._paths) > 1:
		path = solution._paths[1]._path
		edge_path_shortest = [(u, v) for (u, v, d) in G.edges(data=True) if
					 any([u, v] == path[i:i + 2] for i in range(len(path) - 1)) or
					 any([v, u] == path[i:i + 2] for i in range(len(path) - 1))]
	for (u,v) in edge_path_shortest:
		G[u][v]['color'] = 'red'
		G[v][u]['color'] = 'red'

	write_dot(G, 'my_g.dot')

def solve(input, print_graph=False, draw_graph=True):
	solution = Solution()
	infinity = INFINITY
	graph = Graph.from_text(input)
	if print_graph:
		graph.print_graph()
	if draw_graph:
		graph_copy = graph.copy_and_return()
	initial_node_number = graph.get_initial_node()
	dest_node_number = graph.get_dest_node()
	num_of_nodes = graph.get_num_of_nodes()
	k = graph.get_k()

	if initial_node_number > 0 and dest_node_number <= num_of_nodes:
		u = 0
		pathToSelf = False
		found_path = False
		while u < k:
			if dest_node_number in graph.dict_nodes:
				dijkstra = Dijkstra(graph, graph.dict_nodes[initial_node_number].get_number(),
				                    graph.dict_nodes[dest_node_number].get_number())
				if dijkstra.dict_distance_to_initial_node[dest_node_number] < infinity and pathToSelf == False:
					print( "Shortest Path " + str(u + 1) + ": " + str(dijkstra.minimunPathList))
					print( "Path Total Weight: " + str(dijkstra.dict_distance_to_initial_node[dest_node_number]))
					found_path = True
					solution.add_path(u + 1, dijkstra.minimunPathList,
					                  dijkstra.dict_distance_to_initial_node[dest_node_number])
					graph.delete_minor_edge(dijkstra.minimunPathList)
					if dijkstra.dict_distance_to_initial_node[dest_node_number] == 0:
						pathToSelf = True
				else:
					u = k
					if found_path:
						print( "All Possible Paths Found")
					else:
						print("No paths found")
			u = u + 1
	else:
		print("arguments 2 and 3 must be btween 1 and num of nodes")
		
	plot_graph_and_sol(graph_copy, solution)

	return solution


def main():
	sol = solve(
		sys.argv[1]
	)


if __name__ == '__main__':
	main()
