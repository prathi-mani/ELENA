from geopy.geocoders import Nominatim
import networkx as nx
from heapq import heappush, heappop
from itertools import count
from networkx.algorithms.shortest_paths.weighted import _weight_function
from collections import deque
import heapq
import math
import osmnx as ox

def get_coordinates_from_address(coordinates):
    geolocator = Nominatim(user_agent="myapp")
    return geolocator.reverse(coordinates).address

def compute_path_weight(graph, route, weight_attribute):
   total_weight = 0
   for i in range(len(route) - 1):
        total_weight += get_edge_weight(graph, route[i], route[i + 1], weight_attribute)
   return total_weight

def get_edge_weight(graph, node_1, node_2, weight_type="normal"):
    if weight_type == "normal":
        try:
            return graph.edges[node_1, node_2, 0]["length"]
        except KeyError:
            return graph.edges[node_1, node_2]["weight"]

    elif weight_type == "elevation_gain":
        return max(0.0, graph.nodes[node_2]["elevation"] - graph.nodes[node_1]["elevation"])

