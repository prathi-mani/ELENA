import logging
import networkx as nx
import osmnx as ox
from server.model.RouteInfo import RouteInfo
from server.model.utils import compute_path_weight
from server.model.utils import get_coordinates_from_address
from server.model.ModelManager import ModelManager



class PathCalculator:
    def __init__(self, graph):
        self.logger = logging.getLogger(__name__)
        self.graph = graph
        self.initial_location = None
        self.target_location = None

    def fetch_optimal_route(self, starting_point, ending_point):
        graph = self.graph
        self.initial_location, self.target_location = None, None
        self.initial_location= ox.distance.nearest_nodes(graph, starting_point[1], starting_point[0])
        self.target_location = ox.distance.nearest_nodes(graph, ending_point[1], ending_point[0])
        self.closest_route = nx.shortest_path(graph, source=self.initial_location, target=self.target_location, weight='length')
        print("Shortest route between source and destination has been calculated.")

        route_info = RouteInfo()
        
        route_info.origin_location = self.initial_location
       
        route_info.destination_location =  self.target_location
        
        route_info.algoName = "Shortest Route"
        
        route_info.altitude_gain  = compute_path_weight(self.graph, self.closest_route, "elevation_gain")
       
        route_info.altitude_drop = 0
       
        route_info.path = [[graph.nodes[route_node]['x'], graph.nodes[route_node]['y']] for route_node in self.closest_route]
       
        route_info.distance = sum(ox.utils_graph.get_route_edge_attributes(graph, self.closest_route, 'length'))


        return route_info



class Model:
    def __init__(self):
        self.graph = None
        self.obj_algorithm = None
        self.path_limit = None
        self.elevation_strategy = None
        self.obj_elevation_path = None
        self.info_elevation_path = None
        self.optimal_path_object = None
        self.shortest_path_information = None
        self.observer = None
        self.algorithm = None

    def add_observer(self, observer):
        self.observer = observer

    def update_algorithm_object(self):
        self.obj_algorithm = self.algorithm(self.graph, self.shortest_path_information.distance, self.path_limit, self.elevation_strategy, self.shortest_path_information.origin_location, self.shortest_path_information.destination_location, self.shortest_path_information.altitude_gain)

    def update_algorithm(self, algorithm):
        self.algorithm = algorithm

    def compute_paths(self, origin, destination, path_limit, elevation_strategy):
        # calculate shortest path
        self.update_shortest_route_information(origin, destination)
        self.display_route_information(self.shortest_path_information)
        if path_limit == 0:
            self.observer.notify_route_update(self.shortest_path_information, self.shortest_path_information, get_coordinates_from_address(origin), get_coordinates_from_address(destination))
            return
        self.path_limit = path_limit / 100.0
        self.elevation_strategy = elevation_strategy
        self.update_algorithm_object()
        self.info_elevation_path = self.obj_algorithm.fetch_optimal_route()
        self.display_route_information(self.info_elevation_path)
        self.observer.notify_route_update(self.shortest_path_information, self.info_elevation_path, get_coordinates_from_address(origin), get_coordinates_from_address(destination))

    def update_shortest_route_information(self, initial_node, target_node):
        self.graph = ModelManager().analyze_elevation_graph(target_node)
        self.optimal_path_object = PathCalculator(self.graph)
        self.shortest_path_information = self.optimal_path_object.fetch_optimal_route(initial_node, target_node)

    def display_route_information(self, route):
        
        print("Results Details")
        print("Algorithm: " + route.algoName)
        print("Total Distance: " + str(route.distance))
        print("Elevation Gain/Drop: " + str(route.altitude_gain))
      
      
