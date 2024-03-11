# Author: Aiden Nelson
# Date of Last Edit: 3/10/2024
# Purpose: This file implements a comprehensive testing suite for the Mexico Superchargers project.
# It allows any of Floyd-Warshall, Dijkstra's, or A* to be run on different sized graphs of municipalities.
# How to Run: Simply build TestCase objects in the TEST_CASES constant, then run the file.
# It will output shortest paths or distances for each of the TestCases, as well as automatically load graphs.

import json
from definitions import Graph, GraphType, SPAlgorithm, TestCase, Municipality
from aStar import AStar
from dijkstra import Dijkstra
from floydWarshall import FloydWarshall

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
		GraphType.EIGHT_NODES,
		SPAlgorithm.DIJKSTRA
	),
]

# Function to load in initial graph (already given distances, codes, etc.)
def getGraph(graphType: GraphType) -> Graph:
	match graphType:
		case GraphType.ALL_NODES:
			with open('../graphs/allMunicipalitiesGraph.json') as file:
				obj: dict[str, dict] = json.load(file)
				return Graph({code: Municipality(index, **value) for index, (code, value) in enumerate(obj.items())})
		case GraphType.EIGHT_NODES:
			with open('../graphs/eightMunicipalitiesGraph.json') as file:
				obj: dict[str, dict] = json.load(file)
				return Graph({code: Municipality(index, **value) for index, (code, value) in enumerate(obj.items())})
		case _:
			print("The provided graph type in TestCase does not exist, please retry.")
			raise ValueError("Invalid GraphType in TestCase")

# Function to get the shortest path from a given test case
def getShortestPath(testCase: TestCase, graph: Graph) -> float | int:
	# Call the function from the respective file
	match testCase.algorithm:
		case SPAlgorithm.DIJKSTRA:
			return Dijkstra.getShortestPath(testCase.startingMunicipalityCode, testCase.endingMunicipalityCode, graph)
		case SPAlgorithm.A_STAR:
			return AStar.getShortestPath(testCase.startingMunicipalityCode, testCase.endingMunicipalityCode, graph)
		case SPAlgorithm.FLOYD_WARSHALL:
			return FloydWarshall.getShortestPath(testCase.startingMunicipalityCode, testCase.endingMunicipalityCode, graph)
		case _:
			print("Bad algorithm type in test case, please retry.")
			raise ValueError("Invalid algorithm type")

# Main function to run different TestCase objects
def main():
	if not TEST_CASES: return

	# Load in all graphs
	print("Loading all graphs...")
	graphs: dict[GraphType:Graph] = {}
	for graphType in GraphType: graphs[graphType] = getGraph(graphType)
	print("Done loading graphs.")

	# Run all test cases
	print("Beginning running test cases...\n")
	for i, testCase in enumerate(TEST_CASES):
		# Run the specified algorithm on the test case
		print(f"Running test case {i+1} from {testCase.startingMunicipalityCode} to {testCase.endingMunicipalityCode} using {testCase.algorithm.name} on {testCase.graphType.name} graph...")
		results = getShortestPath(testCase, graphs[testCase.graphType])
		print(f"Shortest path(s): {results} total miles\n")
	print("All test cases have been run.")

# Driver function
if __name__ == "__main__":
	main()
