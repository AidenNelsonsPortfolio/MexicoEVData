import time
from typing import Optional
from definitions import Algorithm, Graph, Municipality, Route


class FloydWarshall(Algorithm):
    @staticmethod
    def getShortestPath(
        startingCode: str, endingCode: str, carRange: int, graph: Graph
    ) -> Optional[Route | float]:
        startTime = time.time()

        # # Make adjacency matrix with all infinity values
        # numMuni: int = len(graph)
        # adjMatrix: list[list[float]] = [
        #     [float("inf")] * numMuni for _ in range(numMuni)
        # ]
        # remChargeMatrix: list[list[float]] = [[-1] * numMuni for _ in range(numMuni)]

        # # Set 0 for cells on the diagonal
        # for i in range(numMuni):
        #     adjMatrix[i][i] = 0
        #     remChargeMatrix[i][i] = carRange

        # # Fill adjMatrix with known values
        # for muni in graph.allMunicipalities:
        #     index = muni.index
        #     for edge in muni.edges:
        #         neighborIndex = graph[edge.toMuniCode].index
        #         adjMatrix[index][neighborIndex] = edge.distance
        #         remChargeMatrix[index][neighborIndex] = carRange - edge.distance

        # # Start of Floyd Warshall's algorithm
        # for _ in range(2):
        #     for i in range(numMuni):
        #         for j in range(numMuni):
        #             for k in range(numMuni):
        #                 chargeLostToI: float = carRange - remChargeMatrix[j][i]
        #                 chargeLostFromI: float = carRange - remChargeMatrix[i][k]
        #                 totalChargeLost: float = chargeLostToI + chargeLostFromI

        #                 # If the middle node has a super charger, only cost is from i to k
        #                 if graph.getMunicipalityByIndex(i).hasSupercharger:
        #                     totalChargeLost = chargeLostFromI

        #                 if (
        #                     (adjMatrix[j][i] + adjMatrix[i][k] < adjMatrix[j][k])
        #                     and carRange >= chargeLostToI
        #                     and carRange >= totalChargeLost
        #                 ):
        #                     adjMatrix[j][k] = adjMatrix[j][i] + adjMatrix[i][k]
        #                     remChargeMatrix[j][k] = max(remChargeMatrix[j][k], carRange - totalChargeLost)

        # with open("resultMatrix8.txt", "w") as file:
        #     for row in adjMatrix:
        #         file.write(" ".join(map(str, row)) + "\n")

        # with open("resultChargeMatrix8.txt", "w") as file:
        #     for row in remChargeMatrix:
        #         file.write(" ".join(map(str, row)) + "\n")

        adjRow = []
        remChargeRow = []
        filename = f"resultMatrix{len(graph)}.txt"
        with open(filename, "r") as file:
            i = 0
            for line in file:
                # Only extract the ith row
                if i == graph[startingCode].index:
                    adjRow = list(map(float, line.strip().split()))
                    break
                i += 1

        filename = f"resultChargeMatrix{len(graph)}.txt"
        with open(filename, "r") as file:
            i = 0
            for line in file:
                # Only extract the ith row
                if i == graph[startingCode].index:
                    remChargeRow = list(map(float, line.strip().split()))
                    break
                i += 1

        # Finding a route is not possible, as optimizes for charge, not distance
        startMuni: Municipality = graph[startingCode]
        endMuni: Municipality = graph[endingCode]

        if adjRow[endMuni.index] == float("inf") or remChargeRow[endMuni.index] < 0:
            print(
                "No route between ",
                startMuni.code,
                " and ",
                endMuni.code,
                " exists with charge constraints.",
            )
            return None

        if endMuni.hasSupercharger:
            print("Max charge at destination: ", carRange)
        else:
            print(
                "Max charge at destination: ",
                remChargeRow[endMuni.index],
            )

        endTime = time.time()
        totalTime = endTime - startTime
        print("Total algorithm time: ", totalTime)

        return float(adjRow[endMuni.index])

    @staticmethod
    def getAllShortestPaths(carRange: int, graph: Graph) -> list[list[float]]:
        raise NotImplementedError(
            "Floyd Warshall algorithm does not support all shortest paths."
        )
