import math

print("There are a total of 4 currencies trading")
print("The currencies that are trading are as follows: \n\n0) USD represented as node '0'.")
print("1) CAD represented as node '1'.")
print("2) CHF represented as node '2'.")
print("3) GBP represented as node '3'.")

money = int(input("Enter the starting money: "))

def download():
	graph = {}
	for key in range(1,13):
		conversion_rate = -math.log(float(input("Enter conversion rate: ")))
		start = int(input("Enter the 'FROM' node: "))
		end = int(input("Enter the 'TO' node: "))
		if start != end:
			if start not in graph:
				graph[start] = {}
			graph[start][end] = float(conversion_rate)
	return graph

# Step 1: For each node prepare the destination and predecessor
def initialize(graph, src):
    dest = {} # Stands for destination
    pre = {} # Stands for predecessor
    for node in graph:
        dest[node] = float('Inf') # We start admiting that the rest of nodes are very very far
        pre[node] = None
    dest[src] = 0 # For the source we know how to reach
    return dest, pre
 
def relax(node, neighbour, graph, dest, pre):
    # If the distance between the node and the neighbour is lower than the one I have now
    if dest[neighbour] > dest[node] + graph[node][neighbour]:
        # Record this lower distance
        dest[neighbour]  = dest[node] + graph[node][neighbour]
        pre[neighbour] = node
 
def retrace_negative_loop(pre, start):
	arbitrageLoop = [start]
	next_node = start
	while True:
		next_node = pre[next_node]
		if next_node not in arbitrageLoop:
			arbitrageLoop.append(next_node)
		else:
			arbitrageLoop.append(next_node)
			arbitrageLoop = arbitrageLoop[arbitrageLoop.index(next_node):]
			return arbitrageLoop


def bellman_ford(graph, source):
    dest, pre = initialize(graph, source)
    for i in range(len(graph)-1): #Run this until is converges
        for u in graph:
            for v in graph[u]: #For each neighbour of u
                relax(u, v, graph, dest, pre) #Lets relax it


    # Step 3: check for negative-weight cycles
    for u in graph:
        for v in graph[u]:
        	if dest[v] < dest[u] + graph[u][v]:
        		return(retrace_negative_loop(pre, source))
    return None

paths = []

graph = download()

for key in graph:
	path = bellman_ford(graph, key)
	if path not in paths and not None:
		paths.append(path)

for path in paths:
	if path == None:
		print("No opportunity here!!!")
	else:
		print ("\nStarting with %(money)i in %(currency)s" % {"money":money,"currency":path[0]})

		for i,value in enumerate(path):
			if i+1 < len(path):
				start = path[i]
				end = path[i+1]
				rate = math.exp(-graph[start][end])
				money *= rate
				print ("%(start)s to %(end)s at %(rate)f = %(money)f" % {"start":start,"end":end,"rate":rate,"money":money})
print("\n")