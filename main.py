import sys
from graph import *
from djikstra import *
from solution import Solution


def solve(input):
	solution = Solution()
	infinito = 999999
	input_file = open(input, "r")
	input_iter = input_file.__iter__()
	num_of_nodes = int(input_iter.next())
	k = int(input_iter.next())
	initial_node_number = int(input_iter.next())
	dest_node_number = int(input_iter.next())

	# graph declaration
	graph = Grafo()
	for i in range(num_of_nodes):
		graph.adicionaNodo(i)

	for edge in input_iter:
		parsed_edge = graph.parse_edge(edge)
		graph.add_edge(parsed_edge)

	if initial_node_number > 0 and dest_node_number < 28:
		u = 0
		pathToSelf = False
		while u < k:
			if dest_node_number in graph.listaDeNodos:
				dijkstra = Dijkstra(graph, graph.listaDeNodos[initial_node_number].getNome(),
				                    graph.listaDeNodos[dest_node_number].getNome())
				if dijkstra.dictDistanciaDoNodoInicial[dest_node_number] < infinito and pathToSelf == False:
					print "Shortest Path " + str(u + 1) + ": " + str(dijkstra.minimunPathList)
					print "Path Total Weight: " + str(dijkstra.dictDistanciaDoNodoInicial[dest_node_number])
					solution.add_path(u+1, dijkstra.minimunPathList, dijkstra.dictDistanciaDoNodoInicial[dest_node_number])
					graph.deletaMenorAresta(dijkstra.minimunPathList)
					if dijkstra.dictDistanciaDoNodoInicial[dest_node_number] == 0:
						pathToSelf = True
				else:
					u = k
					print "All Possible Paths Found"
			u = u + 1
	else:
		print "Argumento 2 e 3 de entrada deve ter valores de 0 a 27"

	return solution


def main():

	sol = solve(
		sys.argv[1]
	)


if __name__ == '__main__':
	main()

