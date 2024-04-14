from dataclasses import dataclass
from enum import Enum
import os
from pathlib import Path
from os import path
from typing import List, Optional

PROJECT_ROOT = str(path.dirname(Path(__file__).parent))
TESTING_DIR = str(path.join(PROJECT_ROOT, 'testing'))

RESULT_MATRICES = [
    path.join(PROJECT_ROOT, 'testing', 'resultChargeMatrix8.txt'),
    path.join(PROJECT_ROOT, 'testing', 'resultChargeMatrix100.txt'),
    path.join(PROJECT_ROOT, 'testing', 'resultChargeMatrix500.txt'),
    path.join(PROJECT_ROOT, 'testing', 'resultChargeMatrix1000.txt'),
    path.join(PROJECT_ROOT, 'testing', 'resultChargeMatrix2475.txt'),
    path.join(PROJECT_ROOT, 'testing', 'resultMatrix8.txt'),
    path.join(PROJECT_ROOT, 'testing', 'resultMatrix100.txt'),
    path.join(PROJECT_ROOT, 'testing', 'resultMatrix500.txt'),
    path.join(PROJECT_ROOT, 'testing', 'resultMatrix1000.txt'),
    path.join(PROJECT_ROOT, 'testing', 'resultMatrix2475.txt'),
]

MATRIX_ARCHIVES = [path.join(
    PROJECT_ROOT, 'archives', f'resultMatrices{x}.zip') for x in range(1, 6)]

# Municipality and MunicipalityEdge classes


class MunicipalityEdge:
    def __init__(
        self, fromMuniCode: str, toMuniCode: str, distance: float | int | None = None
    ):
        self.fromMuniCode = fromMuniCode
        self.toMuniCode = toMuniCode
        self.distance = distance

    def __str__(self):
        return (
            str(self.fromMuniCode)
            + " -> "
            + str(self.toMuniCode)
            + ", distance: "
            + str(self.distance)
        )

    def __lt__(self, other):
        return self.distance < other.distance

    def setEdgeDistance(self, distance: float | int | None):
        if not self.distance:
            self.distance = distance


class Municipality:
    def __init__(
        self,
        index: int,
        name: str,
        state: str,
        code: str,
        lat: float,
        lon: float,
        hasSupercharger: bool = False,
        edges: dict | None = None,
    ):
        self.index = index
        self.name = name
        self.state = state
        self.code = code
        self.lat = lat
        self.lon = lon
        self.hasSupercharger = hasSupercharger
        self.neighbors: set[str] | None = (
            set([edge["toMuniCode"] for edge in edges]) if edges else set([])
        )
        self.edges = (
            [
                MunicipalityEdge(
                    edge["fromMuniCode"], edge["toMuniCode"], edge["distance"]
                )
                for edge in edges
            ]
            if edges
            else []
        )

    def __str__(self):
        return (
            self.name
            + ", "
            + self.state
            + ", "
            + self.code
            + ", "
            + str(self.hasSupercharger)
        )


# Graph class (for easy access to graph data)
class Graph:
    def __init__(self, graphData: dict[str, Municipality]):
        self.graphData = graphData
        self.indexToMuni = {
            muni.index: muni for muni in self.allMunicipalities}

    def __len__(self):
        return len(self.graphData)

    def __getitem__(self, key: str) -> Municipality:
        return self.graphData[key]

    @ property
    def allMunicipalityCodes(self) -> set[str]:
        return set(self.graphData.keys())

    @ property
    def allMunicipalities(self) -> list[Municipality]:
        return list(self.graphData.values())

    def getRawGraph(self) -> dict[str, Municipality]:
        return self.graphData

    def getMunicipality(self, muniCode: str) -> Municipality:
        return self.graphData[muniCode]

    def getMunicipalityByIndex(self, index: int) -> Municipality:
        return self.indexToMuni.get(index, None)

    def getMunicipalityEdges(self, muniCode: str) -> list[MunicipalityEdge]:
        return self.graphData[muniCode].edges

    def getMunicipalityNeighbors(self, muniCode: str) -> set[str]:
        return self.graphData[muniCode].neighbors

    def getMunicipalityHasSupercharger(self, muniCode: str) -> bool:
        return self.graphData[muniCode].hasSupercharger


# Dataclasses for Route and RouteStop (for printing shortest path)
@ dataclass
class RouteStop:
    muniCode: str
    distance: float | int
    charged: bool = False

    def __str__(self):
        return f"{self.muniCode} (Edge Distance: {self.distance:.2f}, Charged: {self.charged})"


# Enums for GraphType and SPAlgorithm (for use in TestCase definitions)
class SPAlgorithm(str, Enum):
    DIJKSTRA = "Dijkstras"
    A_STAR = "A*"
    FLOYD_WARSHALL = "Floyd Warshall"


class GraphType(str, Enum):
    ALL_NODES = "All nodes in the graph"
    EIGHT_NODES = "Eight nodes in the graph"
    FIVE_HUNDRED_NODES = "Five hundred nodes in the graph"
    ONE_THOUSAND_NODES = "One thousand nodes in the graph"
    ONE_HUNDRED_NODES = "One hundred nodes in the graph"


# Dataclass for TestCase (to be used in testSuite.py)
@ dataclass
class TestCase:
    startingMunicipalityCode: str
    endingMunicipalityCode: str
    graphType: GraphType


@ dataclass
class Route:
    def __init__(self, stops: Optional[List[RouteStop]], algorithm: SPAlgorithm):
        self.stops: Optional[list[RouteStop]] = stops
        self.algorithm: SPAlgorithm = algorithm

    def __str__(self):
        return (
            ""
            if not self.stops
            else " -> ".join(
                [
                    f'{str(stop)}{os.linesep if i % 2 == 0 else ""}'
                    for (i, stop) in enumerate(self.stops)
                ]
            )
        )

    def __len__(self):
        return len(self.stops)

    @ property
    def totalDistance(self):
        return sum([stop.distance for stop in self.stops]) if self.stops else 0

    def reverse(self):
        self.stops.reverse()

    def addStop(self, stop: RouteStop):
        self.stops.append(stop)

    def print_shortest_path_str(self):
        self._print_green(
            f"Shortest path(s): {self.totalDistance:.2f} total miles\n")
        return self

    def print(self):
        self._print_green(str(self))
        return self

    def _print_green(self, str):
        print(f"\033[92m{str}\033[00m")


# Graph Algorithm parent class (standard interface)
class Algorithm:
    @ staticmethod
    def getShortestPath(
        startingCode: str, endingCode: str, carRange: int, graph: Graph
    ) -> Optional[Route | float]:
        raise NotImplementedError("Subclasses must implement getShortestPath.")


# Enum for each model Tesla car (to be used in testing)
class TeslaModelRange(Enum):
    MODEL_Y = 260
    MODEL_3 = 272
    MODEL_X = 335
    CYBERTRUCK = 340
    MODEL_S = 402
