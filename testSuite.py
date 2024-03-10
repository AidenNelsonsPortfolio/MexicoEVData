# Author: Aiden Nelson
# Date of Last Edit: 3/9/2024
# Purpose: This file implements a comprehensive testing suite for the Mexico Superchargers project.
# It allows any of Floyd-Warshall, Dijkstra's, or A* to be run on different sized graphs of municipalities.
# How to Run: Simply build TestCase objects in the TEST_CASES constant, then run the file.
# It will output shortest paths or distances for each of the TestCases, as well as automatically load graphs.

import json
from dataclasses import dataclass
from enum import Enum

# Graph and Test Case Classes
class MunicipalityEdge:
	def __init__(self, fromMuniCode:str, toMuniCode:str, distance:float|int|None=None):
		self.fromMuniCode = fromMuniCode
		self.toMuniCode = toMuniCode
		self.distance = distance

	def __str__(self):
		return str(self.fromMuniCode) + " -> " + str(self.toMuniCode) + ", distance: " + str(self.distance)

	def __lt__(self, other):
		return self.distance < other.distance

	def setEdgeDistance(self, distance:float|int|None):
		if not self.distance:
			self.distance = distance

class Municipality:
	def __init__(self, index:int, name:str, state:str, code:str, lat:float, lon:float, hasSupercharger:bool=False, edges:dict|None=None):
		self.index = index
		self.name = name
		self.state = state
		self.code = code
		self.lat = lat
		self.lon = lon
		self.hasSupercharger = hasSupercharger
		self.neighbors: set[str]|None = set([edge["toMuniCode"] for edge in edges]) if edges else set([])
		self.edges = [MunicipalityEdge(
			edge["fromMuniCode"], 
			edge["toMuniCode"], 
			edge["distance"]) for edge in edges] if edges else []
	
	def __str__(self):
		return self.name + ", " + self.state + ", " + self.code + ", " + str(self.hasSupercharger)

class SPAlgorithm(Enum):
	DIJKSTRA = 0
	A_STAR = 1
	FLOYD_WARSHALL = 2

class GraphType(Enum):
	ALL_NODES = 0
	EIGHT_NODES = 1

@dataclass
class TestCase:
	startingMunicipalityCode: str
	endingMunicipalityCode: str | None
	graphType: GraphType
	algorithm: SPAlgorithm


# Defined Test Cases and other Constants
TEST_CASES: list[TestCase] | None = [
	TestCase(
		"07076",
		"12035",
		GraphType.EIGHT_NODES,
		SPAlgorithm.FLOYD_WARSHALL
	),
	TestCase(
		"07076",
		"12035",
		GraphType.ALL_NODES,
		SPAlgorithm.FLOYD_WARSHALL
	),
]


# Function to load in initial graph (already given distances, codes, etc.)
def getGraph(graphType: GraphType) -> dict[str, Municipality]:
	match graphType:
		case GraphType.ALL_NODES:
			with open('cleanMunicipalitiesWithEdgesV2.json') as file:
				obj: dict[str, dict] = json.load(file)
				return {code: Municipality(index, **value) for index, (code, value) in enumerate(obj.items())}
		case GraphType.EIGHT_NODES:
			with open('8municipalities.json') as file:
				obj: dict[str, dict] = json.load(file)
				return {code: Municipality(index, **value) for index, (code, value) in enumerate(obj.items())}
		case _:
			print("The provided graph type in TestCase does not exist, please retry.")
			raise ValueError("Invalid GraphType in TestCase")

# Function to run Floyd-Warshall's Algorithm
def floydWarshall(startingCode: str, endingCode: str, graphData: dict[str, Municipality]):
	# Make adjacency matrix with all infinity values
	numMuni:int = len(graphData)
	adjMatrix: list[list[float]] = [[float('inf')] * numMuni for _ in range(numMuni)]

	# Set 0 for cells on the diagonal
	for i in range(numMuni): adjMatrix[i][i] = 0

	# Fill adjMatrix with known values
	for muni in graphData.values():
		index = muni.index
		edges = muni.edges
		for edge in edges:
			neighbor_index = graphData[edge.toMuniCode].index
			adjMatrix[index][neighbor_index] = edge.distance

	# Start of Floyd Warshall's algorithm 
	for k in range(numMuni):
		for i in range(numMuni):
			for j in range(numMuni):
				if adjMatrix[i][k] + adjMatrix[k][j] < adjMatrix[i][j]:
					adjMatrix[i][j] = adjMatrix[i][k] + adjMatrix[k][j]

	# Find a route
	startMuni: Municipality = graphData[startingCode]
	endMuni: Municipality = graphData[endingCode]
	maxRange: int = 40
	exceededRange: bool = False 

	if adjMatrix[startMuni.index][endMuni.index] == float('inf'):
		print("No route between ", startMuni.code, " and ", endMuni.code, " exists")

	route: list[tuple[str, float|int]] = [(startMuni.code, 0)]

	nextMuni = startMuni
	while nextMuni.index != endMuni.index and not exceededRange:
		for neighbor in nextMuni.neighbors:
			neighborMuni = graphData[neighbor]
			if adjMatrix[nextMuni.index][neighborMuni.index] + adjMatrix[neighborMuni.index][endMuni.index] == adjMatrix[nextMuni.index][endMuni.index]:
				if adjMatrix[nextMuni.index][neighborMuni.index] > maxRange:
					exceededRange = True
					break
				route.append((neighbor, adjMatrix[nextMuni.index][neighborMuni.index]))
				nextMuni = neighborMuni
				break

	if exceededRange:
		print("ERROR: Exceeded range")
		return

	formattedRoute: str = ' -> '.join([f"{code} (Edge Distance: {distance})" for code, distance in route])
	totalDistance: float|int = sum([distance for _, distance in route])
	print(f"The route between {startMuni.code} and {endMuni.code} is: {formattedRoute}.")
	print(f"The total distance is {totalDistance}")

	return totalDistance

# Function to run Dijkstra's Algorithm
def dijkstra(startingCode: str, endingCode: str|None, graphData: dict[str, Municipality]):
	pass

# Function to run A* Algorithm
def aStar(startingCode: str, endingCode: str|None, graphData: dict[str, Municipality]):
	pass

# Function to run a given graph on a defined algorithm
def getShortestPath(testCase: TestCase, graphData: dict[str, Municipality]) -> int | dict[str, int]:
	# Call the function from the respective file
	match testCase.algorithm:
		case SPAlgorithm.DIJKSTRA:
			return dijkstra(testCase.startingMunicipalityCode, testCase.endingMunicipalityCode, graphData)
		case SPAlgorithm.A_STAR:
			return aStar(testCase.startingMunicipalityCode, testCase.endingMunicipalityCode, graphData)
		case SPAlgorithm.FLOYD_WARSHALL:
			if not testCase.endingMunicipalityCode:
				print("Floyd Warshall requires only one destination municipality, please adjust TestCase accordingly.")
				raise ValueError("Invalid Floyd Warshall TestCase")
			return floydWarshall(testCase.startingMunicipalityCode, testCase.endingMunicipalityCode, graphData)
		case _:
			print("Bad algorithm type in test case, please retry.")
			raise ValueError("Invalid algorithm type")

# Main function to run different TestCase objects
def main():
	if not TEST_CASES: return

	# Load in all graphs
	print("Loading all graphs...")
	graphData = {}
	for graphType in GraphType:
		graphData[graphType] = getGraph(graphType)
	print("Done loading graphs.")

	# Run all test cases
	print("Beginning running test cases...\n")
	for i, testCase in enumerate(TEST_CASES):
		# Run the specified algorithm on the test case
		print(f"Running test case {i+1} from {testCase.startingMunicipalityCode} to {testCase.endingMunicipalityCode}...")
		results = getShortestPath(testCase, graphData[testCase.graphType])
		print(f"Shortest path(s): {results}\n")
	print("All test cases have been run.")

# Driver function
if __name__ == "__main__":
	main()
