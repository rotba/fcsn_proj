#calculates the factors vector that aggregates multiple values weight to a single value weight
def calc_aggregation_vector(graph):
	num_of_weights = graph.number_of_weights
	ans = []*num_of_weights
	ans [0] = 0
	for i in [1, num_of_weights-1]:
		proj_w_i = map(e -> graph.W(e)[i], graph.E) # projection of the i'th weights over all the edges weights
		ans[i] = celing(log(sum(proj_w_i))) + ans[i-1]
	ans = map(x->pow(2,x), ans);
	return ans
	
# reduces the amount of weights per edge to single value weight
def reduce(graph):
	aggregation_vector = calc_aggregation_vector(graph)
	for e in graph.E:
		graph.W(e) = dot_product(aggregation_vector ,graph.W(e))
	return graph

#finds the k shortests paths given a graph with multiple weights over the edegs
def solution(graph, k, source, target):
	graph = reduce(graph) # convert multiple weights to single weight 
	no_more_paths = False  
	ans = {}
	while ans.length < k or no_more_paths
		p = dijkstra(graph, source, target)
		if p is None:
			no_more_paths = True
		else:
			ans.add(p)
			e = find_lightest_edge(p)
			graph.remove(e)
			
	return ans
		
		
		
			
		
		
	