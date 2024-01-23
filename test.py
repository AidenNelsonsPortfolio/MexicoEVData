# This file will attempt to make a graph out of the municipalities in Mexico using the municipalities.json file

import json
import csv

INTERMUNICIPAL_FILE = "intermunicipal_od_2020_01_01.csv"


class Municipality:
    def __init__(self, name, state, code, hasSupercharger=False):
        self.name = name
        self.state = state
        self.code = code
        self.hasSupercharger = hasSupercharger
    
    def __str__(self):
        return self.name + ", " + self.state + ", " + self.code + ", " + str(self.hasSupercharger)


def getMunicipalities(fileName):
    with open(fileName) as file:
        # Remove the geo_shape keys
        municipalities = json.load(file)
        for municipality in municipalities:
            del municipality['geo_shape']
        return municipalities


def cleanMunicipalities():
    print("Opening municipalities.json")
    municipalities = getMunicipalities('municipalities.json')
    print("Municipalities read")

    # Save the municipalities as a json file
    with open('cleanMunicipalities.json', 'w') as file:
        json.dump(municipalities, file)
        
    print("Municipalities saved as cleanMunicipalities.json")


def getMexicoSuperchargerLocations():
    # Open the superchargerLocations.csv file
    with open('superchargerLocations.csv') as file:
        reader = csv.DictReader(file)
        # Iterate over the rows and get the Mexico superchargers
        mexicoSuperchargers = []
        for row in reader:
            if row['Country'] == 'Mexico':
                mexicoSuperchargers.append(row)
        return mexicoSuperchargers


def cleanSuperchargers():
    mexicoSuperchargers = getMexicoSuperchargerLocations()
    print("Mexico superchargers read")
    # Write these to a CSV file titled cleanSuperchargers.csv
    keysToKeep = ['Supercharger', 'City', 'State']
    with open('cleanSuperchargers.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=keysToKeep)
        writer.writeheader()
        for supercharger in mexicoSuperchargers:
            writer.writerow({key: supercharger[key] for key in keysToKeep})
    print("Mexico superchargers saved as cleanSuperchargers.csv")


def cleanIntramunicipal():
    with open(INTERMUNICIPAL_FILE, 'r') as file:
        reader = csv.DictReader(file)

        headers = [field for field in reader.fieldnames if field != 'date']

        # Write the updated header to a new CSV file
        with open('cleanIntramunicipal.csv', 'w', newline='') as newFile:
            writer = csv.DictWriter(newFile, fieldnames=headers)
            writer.writeheader()

            # Process each row
            for row in reader:
                row['from'] = row['from'].replace('.', '0')
                row['to'] = row['to'].replace('.', '0')

                # Remove the 'date' column from the row
                row.pop('date', None)

                # Write the updated row to a new CSV file
                writer.writerow(row)


def loadCleanIntermunicipal():
    with open('cleanIntramunicipal.csv') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def loadCleanMunicipalities():
    with open('cleanMunicipalities.json') as file:
        return json.load(file)


def loadCleanSuperchargers():
    # Read in the CSV so that it is a dictionary
    with open('cleanMexicoSuperchargers.csv') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


# DO NOT USE THIS, WAS DONE MANUALLY AS ENCODING PROVED DIFFICULT
def addMunicipalityColumn():
    # Add a municipality column to the superchargers
    superchargers = loadCleanSuperchargers()
    # Default to the City column
    for supercharger in superchargers:
        supercharger['Municipality'] = supercharger['City']
    # Write the superchargers to a CSV file
    with open('mexicoSuperchargersWithMunicipality.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=superchargers[0].keys())
        writer.writeheader()
        for supercharger in superchargers:
            writer.writerow(supercharger)


def main():
    cleanIntramunicipal()
    # For each supercharger, determine if its city is in the municipalities.json file
    municipalities = loadCleanMunicipalities()
    superchargers = loadCleanSuperchargers()
    
    nameToMunicipality = { municipality['sta_name'][0]+"_"+municipality['mun_name'][0]: Municipality(municipality['mun_name'][0], municipality['sta_name'][0], municipality['mun_code'][0]) for municipality in municipalities }

    # Iterate over the superchargers and see how many of their cities are in the municipalities
    for supercharger in superchargers:
        escapedMunicipality = supercharger['State']+"_"+supercharger['Municipality']
        decodedMunicipality = escapedMunicipality.encode('utf-8').decode('unicode-escape')
        if decodedMunicipality not in nameToMunicipality:
            print("Bad supercharger location: ", decodedMunicipality)
            continue
        municipality = nameToMunicipality[decodedMunicipality]
        municipality.hasSupercharger = True

    totalWithSuperchargers = 0
    for municipality, obj in nameToMunicipality.items():
        if obj.hasSupercharger:
            print(municipality)
            totalWithSuperchargers += 1

    # Should be 32 total
    print("Total with superchargers: ", totalWithSuperchargers)

    print("Done.")


if __name__ == '__main__':
    main()
