# Author: Aiden Nelson
# Date of Last Edit: 3/10/2024
# Purpose: This file implements a comprehensive testing suite for the Mexico Superchargers project.
# It allows any of Floyd-Warshall, Dijkstra's, or A* to be run on different sized graphs of municipalities.
# How to Run: Simply build TestCase objects in the TEST_CASES constant, then run the file.
# It will output shortest paths or distances for each of the TestCases, as well as automatically load graphs.

import json
from os import path
from pathlib import Path
from typing import Optional
from definitions import (
    Graph,
    GraphType,
    Route,
    SPAlgorithm,
    TestCase,
    Municipality,
    TeslaModelRange,
    RESULT_MATRICES,
    PROJECT_ROOT,
    TESTING_DIR,
    MATRIX_ARCHIVES,
)
from zipfile import ZipFile
from aStar import AStar
from dijkstra import Dijkstra
from floydWarshall import FloydWarshall
from testCases import TEST_CASES

# from createMap import createMap

# Defined constants
ALGORITHMS_TO_TEST: list[SPAlgorithm] = [
    SPAlgorithm.DIJKSTRA,
    SPAlgorithm.A_STAR,
    SPAlgorithm.FLOYD_WARSHALL,
]

CARS_TO_TEST: list[TeslaModelRange] = [
    TeslaModelRange.MODEL_Y,
    # TeslaModelRange.MODEL_3,
    # TeslaModelRange.MODEL_X,
    # TeslaModelRange.CYBERTRUCK,
    # TeslaModelRange.MODEL_S,
]


# Function to load in initial graph (already given distances, codes, etc.)
def getGraph(graphType: GraphType) -> Graph:
    parent_dir = str(path.dirname(Path(__file__).parent))
    match graphType:
        case GraphType.ALL_NODES:
            with open(
                path.join(parent_dir, "graphs/allMunicipalitiesGraph.json")
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
        case GraphType.FIVE_HUNDRED_NODES:
            with open(path.join(parent_dir, "graphs/random500Munis.json")) as file:
                obj: dict[str, dict] = json.load(file)
                return Graph(
                    {
                        code: Municipality(index, **value)
                        for index, (code, value) in enumerate(obj.items())
                    }
                )
        case GraphType.ONE_THOUSAND_NODES:
            with open(path.join(parent_dir, "graphs/random1000Munis.json")) as file:
                obj: dict[str, dict] = json.load(file)
                return Graph(
                    {
                        code: Municipality(index, **value)
                        for index, (code, value) in enumerate(obj.items())
                    }
                )
        case GraphType.ONE_HUNDRED_NODES:
            with open(
                path.join(parent_dir, "graphs/100MunicipalitiesGraph.json")
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


def noRouteErrHandler(
    route: Optional[Route | float], algo: SPAlgorithm
) -> Optional[Route | float]:
    if not isinstance(route, float) and not route:
        print(
            "\033[91m-------------------------------------"
        )  # '\033[91m' is ANSI Color Red Opening Character
        print(f"No route found for {algo}")
        print(
            "-------------------------------------\033[00m"
        )  # '\033[00m' is ANSI Color Closing Character
    return route


# Function to get the shortest path from a given test case
def getShortestPath(
    testCase: TestCase, algorithm: SPAlgorithm, carRange: TeslaModelRange, graph: Graph
) -> Optional[Route | float]:
    # Call the function from the respective file
    match algorithm:
        case SPAlgorithm.DIJKSTRA:
            return noRouteErrHandler(
                Dijkstra.getShortestPath(
                    testCase.startingMunicipalityCode,
                    testCase.endingMunicipalityCode,
                    carRange.value,
                    graph,
                ),
                SPAlgorithm.DIJKSTRA,
            )
        case SPAlgorithm.A_STAR:
            return noRouteErrHandler(
                (
                    AStar.getShortestPath(
                        testCase.startingMunicipalityCode,
                        testCase.endingMunicipalityCode,
                        carRange.value,
                        graph,
                    )
                ),
                SPAlgorithm.A_STAR,
            )
        case SPAlgorithm.FLOYD_WARSHALL:
            return noRouteErrHandler(
                FloydWarshall.getShortestPath(
                    testCase.startingMunicipalityCode,
                    testCase.endingMunicipalityCode,
                    carRange.value,
                    graph,
                ),
                SPAlgorithm.FLOYD_WARSHALL,
            )
        case _:
            print("Bad algorithm type in test case, please retry.")
            raise ValueError("Invalid algorithm type")


# Function to get all shortest paths from a given test case
def getAllShortestPaths(
    algorithm: SPAlgorithm, carRange: TeslaModelRange, graph: Graph
) -> list[list[float]]:
    match algorithm:
        case SPAlgorithm.DIJKSTRA:
            return Dijkstra.getAllShortestPaths(carRange.value, graph)
        case SPAlgorithm.A_STAR:
            return AStar.getAllShortestPaths(carRange.value, graph)
        case SPAlgorithm.FLOYD_WARSHALL:
            print("Floyd-Warshall already returns all shortest paths, no need to run.")
            return []
            # return FloydWarshall.getAllShortestPaths(carRange.value, graph)
        case _:
            print("Bad algorithm type in test case, please retry.")
            raise ValueError("Invalid algorithm type")


# Main function to run different TestCase objects
def main():
    if any(map(lambda x: not path.exists(x), RESULT_MATRICES)):
        print("Extracting result matrices...")
        for z in MATRIX_ARCHIVES:
            with ZipFile(z, "r") as m:
                m.extractall(TESTING_DIR)
        print("Done extracting result matrices.")

    if not TEST_CASES:
        return

    # Load in all graphs
    print("Loading all graphs...")
    graphs: dict[GraphType:Graph] = {}
    for graphType in GraphType:
        graphs[graphType] = getGraph(graphType)
    print("Done loading graphs.")

    # Run all test cases on each algorithm and car range
    print("Beginning running test cases...\n")
    for i, testCase in enumerate(TEST_CASES):
        for j, algorithm in enumerate(ALGORITHMS_TO_TEST):
            for carRange in CARS_TO_TEST:
                if (
                    not testCase.startingMunicipalityCode
                    and not testCase.endingMunicipalityCode
                ):
                    # Means we are finding all shortest paths
                    print(
                        f"\033[93mRunning all shortest paths using {algorithm.value} on {testCase.graphType.value} with max range {carRange.value}...\033[00m"
                    )
                    allShortestPaths: list[list[float]] = getAllShortestPaths(
                        algorithm, carRange, graphs[testCase.graphType]
                    )
                    # Write to file
                    with open(
                        f"allShortestPaths_{algorithm.name}_{len(graphs[testCase.graphType])}.txt",
                        "w",
                    ) as file:
                        for row in allShortestPaths:
                            file.write(" ".join(map(str, row)) + "\n")
                else:
                    print(
                        f"\033[93mRunning test case {i+1} from {testCase.startingMunicipalityCode} to {testCase.endingMunicipalityCode} using {algorithm.value} on {testCase.graphType.value} with max range {carRange.value}...\033[00m"
                    )
                    print(
                        f"From: {graphs[testCase.graphType][testCase.startingMunicipalityCode].name}"
                    )
                    print(
                        f"To: {graphs[testCase.graphType][testCase.endingMunicipalityCode].name}"
                    )
                    route: Optional[Route | float] = getShortestPath(
                        testCase, algorithm, carRange, graphs[testCase.graphType]
                    )
                    if isinstance(route, Route) and route:
                        # Print out and save a map of the route (only once per test case)
                        route.print().print_shortest_path_str()
                        """ 
                        # Commented out to avoid creating maps for all test cases
                        if j == 0:
                            print("Creating map...")
                            createMap(
                                graphs[testCase.graphType],
                                route,
                                f"{testCase.startingMunicipalityCode}to{testCase.endingMunicipalityCode}",
                            )
                            print("Map created.")
                        """
                    elif isinstance(route, float):
                        # Print in green if a route was found
                        print(
                            f"\033[92mShortest path(s): {route:.2f} total miles\033[00m\n"
                        )
    print("All test cases have been run.")


# Driver function
if __name__ == "__main__":
    main()
