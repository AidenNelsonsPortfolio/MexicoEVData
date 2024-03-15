import json
import random


def deleteNodesPerCondition(fileName):
    with open(fileName, 'r') as file:
        data = json.load(file)

    nodesToDelete = []

    for code, value in data.items():
        if value['state'] != 'Ciudad de M\u00e9xico': 
            nodesToDelete.append(code)

    for code in nodesToDelete:
        del data[code]

    with open(fileName, 'w') as file:
        json.dump(data, file, indent=4)

def reduceNumNodes(fileName):
    with open(fileName, 'r') as file:
        data = json.load(file)

    nodesToKeep = random.sample(list(data.keys()), 1000)

    dictionaryOfNodesToKeep = {key: data[key] for key in nodesToKeep}

    data = dictionaryOfNodesToKeep

    with open(fileName, 'w') as file:
        json.dump(data, file, indent=4)

def removeEdgesThatGoNowhere(fileName):
    with open(fileName, 'r') as file:
        newData = json.load(file)

    arrayOfMunis = list(newData.keys())

    for munis in newData.values():
        munis['edges'] = [edge for edge in munis['edges'] if edge['toMuniCode'] in arrayOfMunis]

    with open(fileName, 'w') as file:
        json.dump(newData, file, indent=4)

    

fileName = "random1000Munis.json"
#reduceNumNodes(fileName)
#deleteNodesPerCondition(fileName)
removeEdgesThatGoNowhere(fileName)