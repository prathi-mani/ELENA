import networkx as nx
import osmnx as ox
import math
import logging
from server.model.RouteInfo import RouteInfo
from server.model.utils import compute_path_weight
from heapq import heappush, heappop
from itertools import count
from networkx.algorithms.shortest_paths.weighted import _weight_function

class BaseRoute:
    def __init__(self, graph, closest_route, path_limit, elevation_strategy, initial_location, target_location, shortest_elevation_gain):
        self.logger = logging.getLogger(__name__)  # Initialize logger
        self.graph = graph  # Assign graph object
        self.initial_location = initial_location  # Assign starting location
        self.target_location = target_location  # Assign ending location
        self.closest_route = closest_route  # Assign shortest distance
        self.elevation_strategy = elevation_strategy  # Assign elevation strategy
        self.factor_of_scaling = 100  # Initialize scaling factor
        self.shortest_elevation_gain = shortest_elevation_gain  # Assign shortest elevation gain
        self.path_of_elevation = None  # Initialize path of elevation
        self.path_limit = path_limit  # Assign path limit
        self.elevation_distance = None  # Initialize elevation distance
    
    
        
    def compute_optimal_route(self, heuristicval):
        graph = self.graph
        if self.elevation_strategy == "min":
            min_max_factor = 1
        else:
            min_max_factor = -1
        self.path_of_elevation = nx.shortest_path(self.graph, source=self.initial_location, target=self.target_location, weight='length')  # Compute shortest path based on edge length
        while self.factor_of_scaling < 1000:
            print("self.initial_location is ", self.initial_location)
            commoncode_obj = CommonCode()
            
            #path_of_elevation = commoncode_obj.search_algorithm(graph, self.initial_location, self.target_location, None,weight )  
            path_of_elevation = commoncode_obj.fetch_elevated_path_new(graph, source=self.initial_location, target=self.target_location, heuristic=heuristicval, weight=lambda u, v, d: math.exp(min_max_factor * d[0]['length'] * (d[0]['grade'] + d[0]['grade_abs']) / 2) + math.exp(1/self.factor_of_scaling * (d[0]['length'])))

            elevation_distance = sum(ox.utils_graph.get_route_edge_attributes(graph, path_of_elevation, 'length'))
            elevation_gain = compute_path_weight(self.graph, path_of_elevation, "elevation_gain")
            if elevation_distance <= (1 + self.path_limit) * self.closest_route and \
                    min_max_factor*elevation_gain <= min_max_factor*self.shortest_elevation_gain:
                self.path_of_elevation = path_of_elevation
                self.shortest_elevation_gain = elevation_gain
            self.factor_of_scaling *= 5

        #return self.compile_route_info()
        route_info = RouteInfo()
       
        route_info.algoName = self.__class__.__name__
        #print("algoName is", route_info.algoName)
        route_info.altitude_gain = compute_path_weight(self.graph, self.path_of_elevation, "elevation_gain")
       
        route_info.altitude_drop = 0
        
        route_info.path = [[self.graph.nodes[node]['x'], self.graph.nodes[node]['y']] for node in self.path_of_elevation]
       
        route_info.distance = sum(ox.utils_graph.get_route_edge_attributes(self.graph, self.path_of_elevation, 'length'))
        return route_info


class DijkstraRoute(BaseRoute):
    def fetch_optimal_route(self):
        return self.compute_optimal_route(heuristicval=None)

class AstarRoute(BaseRoute):
    def distance(self, a, b):
        # Distance function used for A* algorithm
        return self.graph.nodes[a]['dist_from_dest'] * 1 / self.factor_of_scaling

    def fetch_optimal_route(self):
        return self.compute_optimal_route(heuristicval=self.distance)

class CommonCode():
   
    def fetch_elevated_path_new(self,graph, source, target, heuristic=None, weight="weight"):
        if source not in graph or target not in graph:
            print("Error: The source or target location is not found in the graph.")
            return None

        if heuristic is None:
            def heuristic(u, v):
                return 0

    # Utilizing the predefined _weight_function
        weight_func = _weight_function(graph, weight)

        push, pop = heappush, heappop
        counter = count()
        queue = [(0, next(counter), source, 0, None)]
        enqueued, explored = {}, {}

        while queue:
            _, __, current_node, dist, parent = pop(queue)

            if current_node == target:
                path = [current_node]
                while parent is not None:
                    path.append(parent)
                    parent = explored.get(parent)
                path.reverse()
                return path

            if current_node in explored:
                continue

            explored[current_node] = parent

            for neighbor, edge_data in graph.adj[current_node].items():
                neighbor_cost = dist + weight_func(current_node, neighbor, edge_data)

                if neighbor in enqueued:
                    qcost, _ = enqueued[neighbor]
                    if qcost <= neighbor_cost:
                        continue

                enqueued[neighbor] = (neighbor_cost, heuristic(neighbor, target))
                push(queue, (neighbor_cost + heuristic(neighbor, target), next(counter), neighbor, neighbor_cost, current_node))

        raise nx.NetworkXNoPath(f"Node {target} not reachable from {source}")




