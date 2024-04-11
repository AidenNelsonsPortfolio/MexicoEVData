import numpy as np

def searchMatrix(fileName):
    validRoutes = []
    
    with open(fileName, 'r') as file:
        lines = file.readlines()
    
    for i, line in enumerate(lines):
        values = [float(x) for x in line.split()]
        for j, value in enumerate(values):
            if value != 0 and not np.isinf(value):
                validRoutes.append((i, j))
    
    return validRoutes

fileName = 'resultMatrix1000.txt'
validRoutesIndex = searchMatrix(fileName)

with open('validIndices1000.txt', 'w') as output_file:
    for index in validRoutesIndex:
        output_file.write(f"{index}\n")
