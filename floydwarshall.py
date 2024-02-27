import json
    
with open('8municipalities.json') as f: 
    data = json.load(f)

municipalityDictionary = {}

index = 0 
for municipality_code, municipality_info in data.items():
    code = municipality_info['code']
    edges = municipality_info['edges']

    listOfNeighbors = []
    distanceToNeighbors = []

    for edge in edges:
        listOfNeighbors.append(edge['toMuniCode'])
        distanceToNeighbors.append(edge['distance'])

    tempMuniDictionary = {
        "code": code,
        "index": index,
        "toMuniCode": listOfNeighbors,
        "distance": distanceToNeighbors
    }
    index += 1

    municipalityDictionary[municipality_code] = tempMuniDictionary

#make adjacency matrix with all infinity values
numMuni = len(municipalityDictionary)
adjMatrix = [[float('inf')] * numMuni for _ in range(numMuni)]

# Set 0 for cells on the diagonal
for i in range(numMuni):
    adjMatrix[i][i] = 0

# Fill adjMatrix with known values
for municipality_code, municipality_info in municipalityDictionary.items():
    code = municipality_info['code']
    index = municipality_info['index']
    neighbors = municipality_info['toMuniCode']
    distances = municipality_info['distance']

    for neighbor, distance in zip(neighbors, distances):
        neighbor_index = list(municipalityDictionary.keys()).index(neighbor)
        adjMatrix[index][neighbor_index] = distance

# print("\nAdjacency matrix before Floyd-Warshall algorithm:")
# for row in adjMatrix:
#     print(row)

#start of Floyd Warshall's algorithm 
for k in range(numMuni):
    for i in range(numMuni):
        for j in range(numMuni):
            if adjMatrix[i][k] + adjMatrix[k][j] < adjMatrix[i][j]:
                adjMatrix[i][j] = adjMatrix[i][k] + adjMatrix[k][j]
 

# print("\nAdjacency matrix after Floyd-Warshall algorithm:")
# for row in adjMatrix:
#     print(row)

#find a route
start = municipalityDictionary['06004']
end = municipalityDictionary['08010']
maxRange = 40
exceededRange = False 

if adjMatrix[start['index']][end['index']] == float('inf'):
    print("No route between ", start['code'], " and ", end['code'], " exists")

route = [start['code']]
distance = [0]

nextCity = start
while nextCity['index'] != end['index'] and exceededRange == False:
    for neighbor in nextCity['toMuniCode']:
        neighbor_city = municipalityDictionary[neighbor]
        if adjMatrix[nextCity['index']][neighbor_city['index']] + adjMatrix[neighbor_city['index']][end['index']] == adjMatrix[nextCity['index']][end['index']]:
            route.append(neighbor)
            if adjMatrix[nextCity['index']][neighbor_city['index']] > maxRange:
                exceededRange = True
                print("Exceeded range")
                break 
            distance.append(adjMatrix[nextCity['index']][neighbor_city['index']])
            nextCity = neighbor_city 
            break
    
print("The route between ", start['code'], " and ", end['code'], " is:")
print(route)
print("The distance between each city is:")
print(distance)
print("The total distance is {}".format(sum(distance)))