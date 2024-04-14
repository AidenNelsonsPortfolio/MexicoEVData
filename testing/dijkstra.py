# Austin Herkert
# CS 456 Project
# Project - Superchargers in Mexico
# Team - Baby Yoda

import heapq
from typing import Optional
from definitions import Algorithm, Graph, Route, RouteStop, SPAlgorithm


class Dijkstra(Algorithm):
    @staticmethod
    def getShortestPath(
        startingCode: str, endingCode: str, carRange: int, graph: Graph
    ) -> Optional[Route | float]:
        # Create empty dictionary to keep track of distances to other municipalities
        distances = {}
        # Empty dictionary to store the previous municipality, so we can trace the the path back from the starting municipality
        previousShortestDistMuni = {}
        prevMostChargedMuni = {}
        # Empty dictionary to store if the municipality was charged at
        charged = {}
        # Dictionary to store max charge at each municipality
        maxCharge = {}
        # Boolean to check if at least one path exists
        atLeastOnePath = False

        # Set all distances to infinity
        for node in graph.allMunicipalityCodes:
            distances[node] = float("inf")
            maxCharge[node] = -1

        # Set starting municipality distance to zero and charge to full
        distances[startingCode] = 0
        maxCharge[startingCode] = carRange

        # Add the starting municipality to the minimum priority queue
        minPriorityQ: list[tuple[float, str, float]] = [(0, startingCode, carRange)]

        # Keep looping until min priority queue is empty
        while minPriorityQ:
            # Pop off municipality that has the lowest current distance from the queue
            currentDist, currentMuni, currentRange = heapq.heappop(minPriorityQ)

            # If the current distance is not better than the distance already found
            # and if the current available charge is <= the max charge at the municipality, continue
            if (
                currentDist > distances[currentMuni]
                and currentMuni in maxCharge
                and maxCharge[currentMuni] > currentRange
            ):
                continue

            # If it is the ending municipality, then continue
            if currentMuni == endingCode:
                atLeastOnePath = True

            # Loop through the neighbor municipalities of the current municipality
            for edge in graph.getMunicipalityEdges(currentMuni):
                neighborMuni, addedEdge = edge.toMuniCode, edge.distance

                # Subtract the distance to the neighbor and update the range
                updatedRange: float = currentRange - addedEdge

                # If the added edge does not cause the range to be exceeded, then add the edge
                if updatedRange < 0:
                    continue

                # If the neighbor municipality has a Supercharger then reset the range back to full
                if graph.getMunicipalityHasSupercharger(neighborMuni):
                    charged[neighborMuni] = True
                    updatedRange = carRange
                else:
                    charged[neighborMuni] = False
                distance = currentDist + addedEdge

                # If the distance with the added edge is shorter than the shortest distance we have so far, then update the distance to the new shortest distance
                if (
                    distance < distances[neighborMuni]
                    or updatedRange > maxCharge[neighborMuni]
                ):
                    if updatedRange > maxCharge[neighborMuni]:
                        maxCharge[neighborMuni] = updatedRange
                        prevMostChargedMuni[neighborMuni] = currentMuni

                    if distance < distances[neighborMuni]:
                        distances[neighborMuni] = distance
                        previousShortestDistMuni[neighborMuni] = currentMuni

                    # Push the updated distance and range for the municipality onto the queue
                    heapq.heappush(minPriorityQ, (distance, neighborMuni, updatedRange))

        if not atLeastOnePath:
            # If the ending municipality is not found, then return None
            print(
                "ERROR, no suitable route between ",
                startingCode,
                " and ",
                endingCode,
                " exists.",
            )
            return None

        shortestRoute: Route = Route(stops=[], algorithm=SPAlgorithm.DIJKSTRA)
        currentMuni = endingCode
        # First minimize the distance to the ending municipality
        while currentMuni != startingCode:
            shortestRoute.addStop(
                RouteStop(currentMuni, distances[currentMuni], charged[currentMuni])
            )
            currentMuni = previousShortestDistMuni[currentMuni]
        shortestRoute.addStop(RouteStop(startingCode, 0))
        shortestRoute.reverse()

        # Now store max range at each municipality
        print("Max charge at destination: ", maxCharge[endingCode])

        currentDistance = 0
        # Update to have per-edge distances (specific to Dijkstra's)
        for i in range(len(shortestRoute.stops)):
            shortestRoute.stops[i].distance = (
                distances[shortestRoute.stops[i].muniCode] - currentDistance
            )
            currentDistance += shortestRoute.stops[i].distance

        return shortestRoute


# # Function to print the shortest path from one municipality to another using the information gathered from running Dijkstra's Algorithm
# def PrintShortestPath(previousMuni, graphDict, startMuni, endMuni):
#     # If the start and end are the same, then return start municipality
#     if(startMuni == endMuni):
#         return print(graphDict[startMuni].get("name"))

#     # Create an empty list to store the path from the starting municipality to the end municipality
#     path = []
#     # Add the ending municipality to the list
#     path.append(endMuni)
#     # Start with the end municipality as the key
#     currentMuni = endMuni
#     # Starting at the end, work backwards from the end municipality to the previous edges until you get to the starting municipality
#     while previousEdge[currentMuni] != startMuni:
#         path.append(previousMuni[currentMuni])
#         currentMuni = previousMuni[currentMuni]
#     # Add the starting municipality
#     path.append(startMuni)
#     index = len(path) - 1
#     # Reverse the order of the list, so it is start to finish
#     for items in path:
#         # Print out path of municipalities
#         print(graphDict[path[index]].get("name"))
#         index = index - 1
