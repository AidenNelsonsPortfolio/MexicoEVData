from definitions import Algorithm, Graph, Municipality, Route, RouteStop, MAX_RANGE

class FloydWarshall(Algorithm):
	@staticmethod
	def getShortestPath(startingCode: str, endingCode: str, graph: Graph) -> float|int|None:
		# Make adjacency matrix with all infinity values
		numMuni:int = len(graph)
		adjMatrix: list[list[float]] = [[float('inf')] * numMuni for _ in range(numMuni)]

		# Set 0 for cells on the diagonal
		for i in range(numMuni): adjMatrix[i][i] = 0

		# Fill adjMatrix with known values
		for muni in graph.allMunicipalities:
			index = muni.index
			for edge in graph.getMunicipalityEdges(muni.code):
				neighborIndex = graph[edge.toMuniCode].index
				adjMatrix[index][neighborIndex] = edge.distance

		# Start of Floyd Warshall's algorithm 
		for i in range(numMuni):
			for j in range(numMuni):
				for k in range(numMuni):
					if adjMatrix[j][i] + adjMatrix[i][k] < adjMatrix[j][k]:
						adjMatrix[j][k] = adjMatrix[j][i] + adjMatrix[i][k]

		# Find a route
		startMuni: Municipality = graph[startingCode]
		endMuni: Municipality = graph[endingCode]
		exceededRange: bool = False 
		distWithoutCharge: float|int = 0

		if adjMatrix[startMuni.index][endMuni.index] == float('inf'):
			print("No route between ", startMuni.code, " and ", endMuni.code, " exists")

		route: Route = Route([RouteStop(startMuni.code, 0)])

		nextMuni = startMuni
		while nextMuni.index != endMuni.index and not exceededRange:
			for neighbor in graph.getMunicipalityNeighbors(nextMuni.code):
				neighborMuni: Municipality = graph[neighbor]
				if adjMatrix[nextMuni.index][neighborMuni.index] + adjMatrix[neighborMuni.index][endMuni.index] == adjMatrix[nextMuni.index][endMuni.index]:

					if not neighborMuni.hasSupercharger:
						distWithoutCharge += adjMatrix[nextMuni.index][neighborMuni.index]
						route.addStop(RouteStop(neighbor, adjMatrix[nextMuni.index][neighborMuni.index]))
					else: 
						distWithoutCharge = 0
						route.addStop(RouteStop(neighbor, adjMatrix[nextMuni.index][neighborMuni.index], True))

					if distWithoutCharge > MAX_RANGE:
						exceededRange = True
						break

					nextMuni = neighborMuni
					break

		if exceededRange:
			print("ERROR: Exceeded range")
			return None

		print(f"The route between {startMuni.code} and {endMuni.code} is: {route}")
		print(f"Began with range of {MAX_RANGE} mile(s) and finished with range remaining of {MAX_RANGE - distWithoutCharge} mile(s).")

		return route.totalDistance
