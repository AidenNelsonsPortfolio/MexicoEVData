# Austin Herkert
# CS 456 Project
# Project - Superchargers in Mexico
# Team - Baby Yoda

import heapq
from definitions import Algorithm, Graph, Route, RouteStop, MAX_RANGE

class Dijkstra(Algorithm):
	@staticmethod
	def getShortestPath(startingCode: str, endingCode: str, graph: Graph) -> float|int|None:
		# Create empty dictionary to keep track of distances to other municipalities
		distances = {}
		# Empty dictionary to store the previous municipality, so we can trace the the path back from the starting municipality
		previousMuni = {}
		# Empty dictionary to store if the municipality was charged at 
		charged = {}

		# Set all distances to infinity 
		for node in graph.allMunicipalityCodes:
			distances[node] = float('infinity')

		# Set starting municipality distance to zero
		distances[startingCode] = 0

		# Add the starting municipality to the minimum priority queue
		minPriorityQ = [(0, startingCode, MAX_RANGE)]
		endingRange:int = -1

		# Keep looping until min priority queue is empty
		while minPriorityQ:
			# Pop off municipality that has the lowest current distance from the queue
			currentDist, currentMuni, currentRange = heapq.heappop(minPriorityQ)

			# If the current distance is not better than the distance already found then continue, so you do not need to keep exploring
			if currentDist > distances[currentMuni]:
				continue

			# If it is the ending municipality, then return the distance to the ending municipality
			if currentMuni == endingCode: 
				endingRange = currentRange
				break

			# Loop through the neighbor municipalities of the current municipality
			for edge in graph.getMunicipalityEdges(currentMuni):
				neighborMuni, addedEdge = edge.toMuniCode, edge.distance
				# Find out whether or not the neighbor municipality has a Supercharger 
				hasSupercharger: bool = graph.getMunicipalityHasSupercharger(neighborMuni)
				# Subtract the distance to the neighbor and update the range
				updatedRange: float = currentRange - addedEdge

				# If the neighbor municipality has a Supercharger then reset the range back to full
				if hasSupercharger:
					charged[neighborMuni] = True
					updatedRange = MAX_RANGE
				else: charged[neighborMuni] = False

				# If the added edge does not cause the range to be exceeded, then add the edge
				if updatedRange >= 0:
					distance = currentDist + addedEdge
					# If the distance with the added edge is shorter than the shortest distance we have so far, then update the distance to the new shortest distance 
					if distance < distances[neighborMuni]:
						distances[neighborMuni] = distance
						# Update the value to be the previous edge of the neighbor for the shortest path
						previousMuni[neighborMuni] = currentMuni
						# Push the updated distance and range for the municipality onto the queue
						heapq.heappush(minPriorityQ, (distance, neighborMuni, updatedRange))
		else:
			# If the ending municipality is not found, then return None
			print("ERROR, no suitable route between ", startingCode, " and ", endingCode, " exists.")
			return None

		route: Route = Route([])
		currentMuni = endingCode
		while currentMuni != startingCode:
			route.addStop(RouteStop(currentMuni, distances[currentMuni], charged[currentMuni]))
			currentMuni = previousMuni[currentMuni]
		route.addStop(RouteStop(startingCode, 0))
		route.reverse()

		currentDistance = 0
		# Update to have per-edge distances (specific to Dijkstra's)
		for i in range(len(route.stops)):
			route.stops[i].distance = distances[route.stops[i].muniCode] - currentDistance
			currentDistance += route.stops[i].distance

		print(f"The route between {startingCode} and {endingCode} is: {route}")
		print(f"Began with range of {MAX_RANGE} mile(s) and finished with range remaining of {endingRange} mile(s).")
		return route.totalDistance

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
