from dataclasses import dataclass
from enum import Enum
from abc import ABC

MAX_RANGE: int = 35

# Municipality and MunicipalityEdge classes
class MunicipalityEdge:
	def __init__(self, fromMuniCode:str, toMuniCode:str, distance:float|int|None=None):
		self.fromMuniCode = fromMuniCode
		self.toMuniCode = toMuniCode
		self.distance = distance

	def __str__(self):
		return str(self.fromMuniCode) + " -> " + str(self.toMuniCode) + ", distance: " + str(self.distance)

	def __lt__(self, other):
		return self.distance < other.distance

	def setEdgeDistance(self, distance:float|int|None):
		if not self.distance:
			self.distance = distance

class Municipality:
	def __init__(self, index:int, name:str, state:str, code:str, lat:float, lon:float, hasSupercharger:bool=False, edges:dict|None=None):
		self.index = index
		self.name = name
		self.state = state
		self.code = code
		self.lat = lat
		self.lon = lon
		self.hasSupercharger = hasSupercharger
		self.neighbors: set[str]|None = set([edge["toMuniCode"] for edge in edges]) if edges else set([])
		self.edges = [MunicipalityEdge(
			edge["fromMuniCode"], 
			edge["toMuniCode"], 
			edge["distance"]) for edge in edges] if edges else []
	
	def __str__(self):
		return self.name + ", " + self.state + ", " + self.code + ", " + str(self.hasSupercharger)

# Graph class (for easy access to graph data)
class Graph:
	def __init__(self, graphData: dict[str, Municipality]):
		self.graphData = graphData

	def __len__(self):
		return len(self.graphData)
	
	def __getitem__(self, key: str) -> Municipality:
		return self.graphData[key]

	@property
	def allMunicipalityCodes(self) -> set[str]:
		return set(self.graphData.keys())
	
	@property
	def allMunicipalities(self) -> list[Municipality]:
		return list(self.graphData.values())

	def getRawGraph(self) -> dict[str, Municipality]:
		return self.graphData

	def getMunicipality(self, muniCode: str) -> Municipality:
		return self.graphData[muniCode]

	def getMunicipalityEdges(self, muniCode: str) -> list[MunicipalityEdge]:
		return self.graphData[muniCode].edges

	def getMunicipalityNeighbors(self, muniCode: str) -> set[str]:
		return self.graphData[muniCode].neighbors

	def getMunicipalityHasSupercharger(self, muniCode: str) -> bool:
		return self.graphData[muniCode].hasSupercharger

# Graph Algorithm parent class (standard interface)
class Algorithm(ABC):
	@staticmethod
	def getShortestPath(startingCode: str, endingCode: str, graph: Graph) -> float|int|None:
		raise NotImplementedError("Subclasses must implement getShortestPath.")


# Dataclasses for Route and RouteStop (for printing shortest path)
@dataclass
class RouteStop:
	muniCode: str
	distance: float|int
	charged: bool=False

	def __str__(self):
		return f"{self.muniCode} (Edge Distance: {self.distance}, Charged: {self.charged})"

@dataclass
class Route:
	stops: list[RouteStop]

	def __str__(self):
		return ' -> '.join([str(stop) for stop in self.stops])

	def __len__(self):
		return len(self.stops)

	@property
	def totalDistance(self):
		return sum([stop.distance for stop in self.stops])

	def reverse(self):
		self.stops.reverse()

	def addStop(self, stop: RouteStop):
		self.stops.append(stop)

# Enums for GraphType and SPAlgorithm (for use in TestCase definitions)
class SPAlgorithm(Enum):
	DIJKSTRA = 0
	A_STAR = 1
	FLOYD_WARSHALL = 2

class GraphType(Enum):
	ALL_NODES = 0
	EIGHT_NODES = 1

# Dataclass for TestCase (to be used in testSuite.py)
@dataclass
class TestCase:
	startingMunicipalityCode: str
	endingMunicipalityCode: str
	graphType: GraphType
	algorithm: SPAlgorithm
