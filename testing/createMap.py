# This file will create Leaflet maps for the given graph (and highlight a specific path between two nodes)
from definitions import Municipality, Route, RouteStop, Graph
import folium


def createMap(graph: Graph, shortestPath: Route, outputPath):
    # Latitude and Longitude of Mexico City (example)
    latitude, longitude = 19.4326, -99.1332

    # Create a map centered around Mexico
    mexico_map = folium.Map(location=[latitude, longitude], zoom_start=15)

    for muni in graph.allMunicipalities:
        # Add a marker to the map
        folium.Marker([muni.lat, muni.lon], popup=muni.name).add_to(mexico_map)

        # Add a line between the municipality and its neighbors
        for neighbor in muni.neighbors:
            # Get the neighbor
            neighbor = graph.getMunicipality(neighbor)

            # Add a line between the two municipalities
            folium.PolyLine(
                [[muni.lat, muni.lon], [neighbor.lat, neighbor.lon]],
                color="red",
                weight=1,
                opacity=0.5,
            ).add_to(mexico_map)

    # Now highlight the shortest path (weight = 5)
    prevMuni: Municipality = None
    for i, routeStop in enumerate(shortestPath.stops):
        if i == 0:
            prevMuni = graph.getMunicipality(routeStop.muniCode)
        else:
            muni = graph.getMunicipality(routeStop.muniCode)
            folium.PolyLine(
                [[prevMuni.lat, prevMuni.lon], [muni.lat, muni.lon]],
                color="blue",
                weight=10,
                opacity=0.8,
            ).add_to(mexico_map)
            prevMuni = muni

    # Save the map to an HTML file
    mexico_map.save(outputPath + ".html")
    print("Saved interactive map")
