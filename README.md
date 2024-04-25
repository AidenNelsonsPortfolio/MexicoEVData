# CS456 Final Project, Team Baby Yoda

## Overview
This repository contains the entire codebase used in Baby Yoda’s final project. See below for a required Python install, as well as detailed guides on how (and where) to run test cases and data processing.


## Required Python Pip Install
```
pip install folium
```

## How to Run

### Data Pre-Processing (Requires Folium)
This step is largely unnecessary because all of this was done previously and is already properly saved. However, if you would like to re-clean the data, execute the `initialDataProcessing.py` file from the project’s `rawDataProcessing` folder. 
The resulting cleaned data will appear in the same folder `rawDataProcessing`, except the cleaned “graph” of data, which is located at `graphs/allMunicipalitiesGraph.json`.

```
cd rawDataProcessing
python initialDataProcessing.py
```

### Test Suite
When running the test suite, it will run a set of tests on each algorithm, writing each result to the standard out (path, if possible, distance, and execution time).
If you want to modify the number of test cases and or only test specific algorithms follow the instructions below.

#### Add/Remove Test Cases
Edit the `testCases.py` file, we have a variety of test cases defined already, with some commented out.
You can comment or add to the cases like below in the `TEST_CASES` constant. It automatically defaults to the Tesla Model Y for the distance metrics like was outlined in our project report and presentation. This is optional, otherwise the default cases will be used.

> Before
```
TEST_CASES: list[TestCase] = [
	TestCase("24012", "24039", GraphType.FIVE_HUNDRED_NODES),
	# TestCase("20429", "20535", GraphType.FIVE_HUNDRED_NODES),
	# TestCase("20125", "20512", GraphType.FIVE_HUNDRED_NODES),
]
```
> After

```python
TEST_CASES: list[TestCase] = [
	TestCase("24012", "24039", GraphType.FIVE_HUNDRED_NODES),
	TestCase("20429", "20535", GraphType.FIVE_HUNDRED_NODES),
	TestCase("20125", "20512", GraphType.FIVE_HUNDRED_NODES),
]
```

#### Add/Remove Algorithms
Edit the `testSuite.py` file, commenting/uncommenting which algorithm is needed to test in the `ALGORITHMS_TO_TEST` constant. This is optional.

> Before
```
ALGORITHMS_TO_TEST: list[SPAlgorithm] = [
	SPAlgorithm.DIJKSTRA,
	SPAlgorithm.A_STAR,
	# SPAlgorithm.FLOYD_WARSHALL,
]
```
> After
```
ALGORITHMS_TO_TEST: list[SPAlgorithm] = [
	SPAlgorithm.DIJKSTRA,
]
```

#### Add/Remove Cars 
Edit the `testSuite.py` file, commenting/uncommenting which cars you want to test (changes max range each path can have + remaining charge at destination) in the `CARS_TO_TEST` constant. This is optional.

> Before
```
CARS_TO_TEST: list[TeslaModelRange] = [
    TeslaModelRange.MODEL_Y,
    # TeslaModelRange.MODEL_3,
    # TeslaModelRange.MODEL_X,
    # TeslaModelRange.CYBERTRUCK,
    # TeslaModelRange.MODEL_S,
]
```

> After
```
CARS_TO_TEST: list[TeslaModelRange] = [
    TeslaModelRange.MODEL_Y,
    TeslaModelRange.MODEL_3,
    TeslaModelRange.MODEL_X,
    TeslaModelRange.CYBERTRUCK,
    TeslaModelRange.MODEL_S,
]

```
#### Running the Suite
The `testing/testSuite.py` script controls the entire execution of all above defined test cases on all algorithms and cars. It is recommended to run this script from the `testing` folder.
```
cd testing
python testSuite.py
```

#### (Optional) Saving Results to Map (Requires Folium)
If you want to test the "save to map" functionality, where the shortest path between two municipalities is plotted on a visual map of Mexico, you can uncomment line 31 (imports a createMap function) and the code block starting at line 240. 

Running test cases again will save the result of each (if it exists) to a map file in the root directory. **Be warned** this operation can take several seconds PER TEST CASE depending upon the size of the input graph and only works for one to one test cases. Open the static html file in your browser to view the graph (bolded blue line is the shortest path).

### Other Files

#### Graphs Folder
This folder contains the graphs that were manually generated to have different numbers of nodes, and are used in the `testSuite.py` script. Other than the generated `allMunicipalitiesGraph.json` file, none of these should be modified or re-generated.

#### Archives Folder
This contains the saved results for Floyd Warshall (among different graph sizes) so it does not have to be recomputed (as this would take many minutes on each run).
