# Author: Aiden Nelson
# Date of Last Edit: 3/10/2024
# Purpose: This file implements a comprehensive testing suite for the Mexico Superchargers project.
# It allows any of Floyd-Warshall, Dijkstra's, or A* to be run on different sized graphs of municipalities.
# How to Run: Simply build TestCase objects in the TEST_CASES constant, then run the file.
# It will output shortest paths or distances for each of the TestCases, as well as automatically load graphs.

import json
from os import path
from pathlib import Path
import pprint
from typing import Optional
from definitions import Graph, GraphType, Route, SPAlgorithm, TestCase, Municipality
from aStar import AStar
from dijkstra import Dijkstra
from floydWarshall import FloydWarshall

# Defined Test Cases and other Constants
TEST_CASES: list[TestCase] | None = [
    #TestCase("07076", "12035", GraphType.EIGHT_NODES, SPAlgorithm.FLOYD_WARSHALL),
    TestCase("07076", "12035", GraphType.ALL_NODES, SPAlgorithm.FLOYD_WARSHALL)


    #TestCase("07076", "12035", GraphType.EIGHT_NODES, SPAlgorithm.DIJKSTRA),
    #TestCase("07076", "SomeRandomCode", GraphType.EIGHT_NODES, SPAlgorithm.DIJKSTRA),
    #TestCase("07076", "12035", GraphType.ALL_NODES, SPAlgorithm.A_STAR),
    #TestCase("07076", "12035", GraphType.ALL_NODES, SPAlgorithm.DIJKSTRA),
]


# Function to load in initial graph (already given distances, codes, etc.)
def getGraph(graphType: GraphType) -> Graph:
    parent_dir = str(path.dirname(Path(__file__).parent))
    match graphType:
        case GraphType.ALL_NODES:
            with open(
                path.join(parent_dir, "graphs/random1000Munis.json")
            ) as file:
                obj: dict[str, dict] = json.load(file)
                return Graph(
                    {
                        code: Municipality(index, **value)
                        for index, (code, value) in enumerate(obj.items())
                    }
                )
        case GraphType.EIGHT_NODES:
            with open(
                path.join(parent_dir, "graphs/eightMunicipalitiesGraph.json")
            ) as file:
                obj: dict[str, dict] = json.load(file)
                return Graph(
                    {
                        code: Municipality(index, **value)
                        for index, (code, value) in enumerate(obj.items())
                    }
                )
        case _:
            print("The provided graph type in TestCase does not exist, please retry.")
            raise ValueError("Invalid GraphType in TestCase")


def no_route_err_handler(route: Optional[Route], algo: SPAlgorithm):
    if not route:
        print(
            "\033[91m-------------------------------------"
        )  # '\033[91m' is ANSI Color Red Opening Character
        print(f"No route found for {algo}")
        print(
            "-------------------------------------\033[00m"
        )  # '\033[00m' is ANSI Color Closing Character
    return route


# Function to get the shortest path from a given test case
def getShortestPath(testCase: TestCase, graph: Graph) -> Route:
    # Call the function from the respective file
    match testCase.algorithm:
        case SPAlgorithm.DIJKSTRA:
            return no_route_err_handler(
                Dijkstra.getShortestPath(
                    testCase.startingMunicipalityCode,
                    testCase.endingMunicipalityCode,
                    graph,
                ),
                SPAlgorithm.DIJKSTRA,
            )
        case SPAlgorithm.A_STAR:
            return no_route_err_handler(
                (
                    AStar.getShortestPath(
                        testCase.startingMunicipalityCode,
                        testCase.endingMunicipalityCode,
                        graph,
                    )
                ),
                SPAlgorithm.A_STAR,
            )
        case SPAlgorithm.FLOYD_WARSHALL:
            return no_route_err_handler(
                FloydWarshall.getShortestPath(
                    testCase.startingMunicipalityCode,
                    testCase.endingMunicipalityCode,
                    graph,
                ),
                SPAlgorithm.FLOYD_WARSHALL,
            )
        case _:
            print("Bad algorithm type in test case, please retry.")
            raise ValueError("Invalid algorithm type")


# Main function to run different TestCase objects
def main():
    if not TEST_CASES:
        return

    # Load in all graphs
    print("Loading all graphs...")
    graphs: dict[GraphType:Graph] = {}
    for graphType in GraphType:
        graphs[graphType] = getGraph(graphType)
    print("Done loading graphs.")

    # Run all test cases
    print("Beginning running test cases...\n")
    for i, testCase in enumerate(TEST_CASES):
        # Run the specified algorithm on the test case
        print(
            f"\033[93mRunning test case {i+1} from {testCase.startingMunicipalityCode} to {testCase.endingMunicipalityCode} using {testCase.algorithm.value} on {testCase.graphType.value}...\033[00m"
        )
        route = getShortestPath(testCase, graphs[testCase.graphType])
        route.print().print_shortest_path_str() if route else ()
    print("All test cases have been run.")


# Driver function
if __name__ == "__main__":
    main()
