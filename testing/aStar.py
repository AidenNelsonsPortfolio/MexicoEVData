from definitions import (
    Algorithm,
    Graph,
    Municipality,
    Route,
    RouteStop,
    SPAlgorithm,
)
from cmath import sqrt
from math import sqrt, inf
from typing import Callable, Dict, List, Optional
from collections import defaultdict
import heapq
import time


class AStar(Algorithm):
    @staticmethod
    def getShortestPath(
        startingCode: str, endingCode: str, carRange: int, graph: Graph
    ) -> Optional[Route | float]:
        return AStar()._getShortestPath(
            startingCode=startingCode,
            endingCode=endingCode,
            carRange=carRange,
            graph=graph,
        )

    def _getShortestPath(
        self, startingCode: str, endingCode: str, carRange: int, graph: Graph
    ) -> Optional[Route]:
        goal_municpilaity = graph.getMunicipality(endingCode)
        return self._A_Star(
            start=graph.getMunicipality(startingCode),
            end=goal_municpilaity,
            carRange=carRange,
            graph=graph,
            h=self._get_heuristic(goal_municpilaity),
        )

    def _inf_dict(self, negative=False):
        return defaultdict(lambda: inf if not negative else -inf)

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
        self,
        g_scores: Dict[Municipality, Municipality],
        came_from: Dict[Municipality, Municipality],
        start: Municipality,
        end: Municipality,
    ) -> Route:
        shortest_route: Route = Route(stops=[], algorithm=SPAlgorithm.A_STAR)
        cur_muni = end
        while cur_muni != start:
            # Get the next muni and its g_score
            next_muni = came_from[cur_muni]
            prev_g_score = g_scores[next_muni]
            shortest_route.addStop(
                RouteStop(
                    muniCode=cur_muni.code,
                    charged=cur_muni.hasSupercharger,
                    distance=g_scores[cur_muni] - prev_g_score,
                )
            )
            cur_muni = next_muni
        shortest_route.addStop(RouteStop(muniCode=start.code, distance=0))
        shortest_route.reverse()

        return shortest_route

    def _get_heuristic(
        self, goal_state: Municipality
    ) -> Callable[[Municipality], float]:
        return lambda x: self._euc_dist(x, goal_state)

    def _A_Star(
        self,
        start: Municipality,
        end: Municipality,
        carRange: int,
        graph: Graph,
        h: Callable[[Municipality], float],
    ):
        start_time = time.time()

        # Frontier has format: (f_score, chargeRemaining, g_score, municipality)
        frontier: list[tuple[float, float, float, Municipality]] = [
            (h(start), -carRange, 0, start)
        ]

        came_from: Dict[Municipality, Municipality] = {}
        max_charge: Dict[Municipality, float] = self._inf_dict(negative=True)
        g_score: defaultdict[Municipality, float] = self._inf_dict()
        f_score: defaultdict[Municipality, float] = self._inf_dict()

        max_charge[start] = carRange
        g_score[start] = 0
        f_score[start] = h(start)

        # Iterate through frontier
        while frontier:
            # Get the current municipality (rem_charge is negative to make it a max heap)
            cur_f_score, neg_rem_charge, cur_g_score, cur_muni = heapq.heappop(frontier)
            rem_charge = -neg_rem_charge

            if cur_muni.hasSupercharger:
                rem_charge = carRange

            if cur_muni == end:
                print("Max charge at destination: ", max(rem_charge, max_charge[end]))
                print("Total algorithm time: ", time.time() - start_time)
                return self._reconstruct_path(g_score, came_from, start, end)

            for edge in cur_muni.edges:
                neighbor = graph.getMunicipality(edge.toMuniCode)

                tentative_g_score = cur_g_score + edge.distance
                tentative_rem_charge = rem_charge - edge.distance

                if (
                    tentative_g_score < g_score[neighbor]
                    or tentative_rem_charge > max_charge[neighbor]
                ) and tentative_rem_charge >= 0:
                    # Only update "came_from" if the neighbor is a shorter path
                    if tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = cur_muni
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + h(neighbor)
                    if tentative_rem_charge > max_charge[neighbor]:
                        max_charge[neighbor] = tentative_rem_charge
                    heapq.heappush(
                        frontier,
                        (
                            f_score[neighbor],
                            -tentative_rem_charge,
                            tentative_g_score,
                            neighbor,
                        ),
                    )

        print(
            "No route between ",
            start.code,
            " and ",
            end.code,
            " exists with charge constraints.",
        )
        return None
