from definitions import Algorithm, Graph, Municipality, Route, RouteStop, SPAlgorithm
from cmath import sqrt
from math import sqrt, inf
from typing import Callable, Dict, List, Optional
from collections import defaultdict


class AStar(Algorithm):
    @staticmethod
    def getShortestPath(
        startingCode: str, endingCode: str, graph: Graph
    ) -> Optional[Route]:
        return AStar()._getShortestPath(
            startingCode=startingCode, endingCode=endingCode, graph=graph
        )

    def _getShortestPath(
        self, startingCode: str, endingCode: str, graph: Graph
    ) -> Optional[Route]:
        goal_municpilaity = graph.getMunicipality(endingCode)
        return self._A_Star(
            start=graph.getMunicipality(startingCode),
            end=goal_municpilaity,
            all_data=graph.allMunicipalities,
            h=self._get_heuristic(goal_municpilaity),
        )

    def _inf_dict(self):
        return defaultdict(lambda: inf)

    def _euc_dist(self, point1: Municipality, point2: Municipality):
        return float(
            sqrt(abs((point2.lat - point1.lat) ** 2 + (point2.lon - point1.lon) ** 2))
        )

    def _d(
        self,
        from_point: Municipality,
        to_point: Municipality,
        through_point: Municipality,
    ):
        return self._euc_dist(from_point, through_point) + self._euc_dist(
            through_point, to_point
        )

    def _reconstruct_path(
        self, came_from: Dict[Municipality, Municipality], current: Municipality
    ) -> Route:
        total_path = [current]

        while current in came_from.keys():
            current = came_from[current]
            total_path.insert(0, current)

        def calculate_distance(muni, prev_muni):
            for edge in muni.edges:
                if (
                    edge.fromMuniCode == muni.code and edge.toMuniCode == prev_muni.code
                ) or (
                    edge.fromMuniCode == prev_muni.code and edge.toMuniCode == muni.code
                ):
                    return edge.distance
            return 0

        stops = list(
            map(
                lambda muni: RouteStop(
                    muniCode=muni.code,
                    charged=muni.hasSupercharger,
                    distance=sum(
                        calculate_distance(muni, prev_muni)
                        for prev_muni in total_path[: total_path.index(muni)]
                    ),
                ),
                total_path,
            )
        )
        return Route(stops=stops, algorithm=SPAlgorithm.A_STAR)

    def _get_heuristic(
        self, goal_state: Municipality
    ) -> Callable[[Municipality], float]:
        return lambda x: self._euc_dist(x, goal_state)

    def collection_to_single_by_muni(self, to_code: int, nodes: List[Municipality]):
        return next(node for node in nodes if node.code == to_code)

    def _A_Star(
        self,
        start: Municipality,
        end: Municipality,
        all_data: List[Municipality],
        h: Callable[[Municipality], float],
    ):
        open_set = {start}
        came_from: Dict[Municipality, Municipality] = {}

        g_score: defaultdict[Municipality, float] = self._inf_dict()
        g_score[start] = 0

        f_score: defaultdict[Municipality, float] = self._inf_dict()
        f_score[start] = h(start)

        while open_set != {}:
            current = min(open_set, key=lambda n: f_score[n])
            if current == end:
                return self._reconstruct_path(came_from, current)
            open_set.remove(current)
            for edge in current.edges:
                neighbor = self.collection_to_single_by_muni(edge.toMuniCode, all_data)

                tentative_g_score = g_score[current] + self._d(
                    from_point=current, to_point=end, through_point=neighbor
                )
                if tentative_g_score < g_score[neighbor]:

                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + h(neighbor)
                    if neighbor not in open_set:
                        open_set.add(neighbor)

        return None
