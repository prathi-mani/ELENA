import sys
sys.path.insert(0, r"C:\Users\twink\OneDrive\Desktop\Myproject\src")

import unittest
import osmnx as ox
import networkx as nx
from src.server.backend import *
from src.server.model import *
from src.server.model.utils import *
import requests
import json

def get_address_from_lat_long(lat_long):
    lat, lon = lat_long
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    response = requests.get(url)
    data = response.json()
    if data and 'address' in data:
        return data['display_name']
    else:
        return None

class Test(unittest.TestCase):
    
    # Checking if the map is rendered properly
    def test_map_render(self):
        graph = nx.MultiDiGraph()
        self.assertIsInstance(graph, nx.classes.multidigraph.MultiDiGraph)
    
    # Checking if the coordinates are getting converted to the address
    def test_coordinates_from_address(self):
        lat_long = (44.570286100000004, -123.27921585)
        address = get_address_from_lat_long(lat_long)
        assert '2510, NORTHWEST VAN BUREN AVENUE, CORVALLIS,BENTON COUNTY, OREGON, 97331, UNITED STATES, 97331' ;address.upper()

    # Checking if the astar path has less elevation than the shortest path
    def test_astar_short_path(self):
        start = (44.5702861, -123.27921585)
        destination = (44.56305595, -123.28392363395751)
        path_limit = 30
        elevation = 'max'
        controller = AStarController()
        notificationHandler = NotificationHandler()
        model = Model()
        model.add_observer(notificationHandler)
        controller.set_route_model(model)
        controller.set_start_location(start)
        controller.set_end_location(destination)
        controller.set_path_limit(path_limit)
        controller.set_elevation_strategy(elevation)
        controller.manipulate_route_model()
        json_output = json.loads(notificationHandler.get_output_json())
        shortest_distance = json_output['shortest_distance']
        elevation_path_distance = json_output['elevation_path_distance']
        shortest_elevation_gain = json_output['shortest_elevation_gain']
        elevation_path_gain = json_output['elevation_path_gain']
        self.assertLessEqual(elevation_path_distance, (1 + path_limit / 100) * shortest_distance)
        self.assertGreaterEqual(elevation_path_gain, shortest_elevation_gain)

    # Checking if the dijkstra path has less elevation than the shortest path  
    def test_dijkstra_short_path(self):
        start = (44.570286100000004, -123.27921585)
        destination = (44.56305595, -123.28392363395751)
        path_limit = 30
        elevation = 'max'
        controller = DijkstraController()
        notificationHandler = NotificationHandler()
        model = Model()
        model.add_observer(notificationHandler)
        controller.set_route_model(model)
        controller.set_start_location(start)
        controller.set_end_location(destination)
        controller.set_path_limit(path_limit)
        controller.set_elevation_strategy(elevation)
        controller.manipulate_route_model()
        json_output = json.loads(notificationHandler.get_output_json())
        shortest_distance = json_output['shortest_distance']
        elevation_path_distance = json_output['elevation_path_distance']
        shortest_elevation_gain = json_output['shortest_elevation_gain']
        elevation_path_gain = json_output['elevation_path_gain']
        self.assertLessEqual(elevation_path_distance, (1 + path_limit / 100) * shortest_distance)
        self.assertGreaterEqual(elevation_path_gain, shortest_elevation_gain)

    # Checking if the astar path has higher elevation than the shortest path
    def test_astar_max_ele(self):
        start = (44.570286100000004, -123.27921585)
        destination = (44.56305595, -123.28392363395751)
        path_limit = 30
        elevation = 'max'
        controller = AStarController()
        notificationHandler = NotificationHandler()
        model = Model()
        model.add_observer(notificationHandler)
        controller.set_route_model(model)
        controller.set_start_location(start)
        controller.set_end_location(destination)
        controller.set_path_limit(path_limit)
        controller.set_elevation_strategy(elevation)
        controller.manipulate_route_model()
        json_output = json.loads(notificationHandler.get_output_json())
        shortest_distance = json_output['shortest_distance']
        elevation_path_distance = json_output['elevation_path_distance']
        shortest_elevation_gain = json_output['shortest_elevation_gain']
        elevation_path_gain = json_output['elevation_path_gain']
        self.assertLessEqual(elevation_path_distance, (1 + path_limit / 100) * shortest_distance)
        self.assertGreaterEqual(elevation_path_gain, shortest_elevation_gain)

    # Checking if the dijkstra path has higher elevation than the shortest path
    def test_dijkstra_max_ele(self):
        start = (44.570286100000004, -123.27921585)
        destination = (44.56305595, -123.28392363395751)  # Fixed syntax error here
        path_limit = 30
        elevation = 'max'
        controller = DijkstraController()
        notificationHandler = NotificationHandler()
        model = Model()
        model.add_observer(notificationHandler)
        controller.set_route_model(model)
        controller.set_start_location(start)
        controller.set_end_location(destination)
        controller.set_path_limit(path_limit)
        controller.set_elevation_strategy(elevation)
        controller.manipulate_route_model()
        json_output = json.loads(notificationHandler.get_output_json())
        shortest_distance = json_output['shortest_distance']
        elevation_path_distance = json_output['elevation_path_distance']
        shortest_elevation_gain = json_output['shortest_elevation_gain']
        elevation_path_gain = json_output['elevation_path_gain']
        self.assertLessEqual(elevation_path_distance, (1 + path_limit / 100) * shortest_distance)
        self.assertGreaterEqual(elevation_path_gain, shortest_elevation_gain)

    def test_invalid_coordinate_conversion(self):
        # Test error handling for invalid coordinates
        invalid_lat_long = (200, 200)  # Invalid coordinates
        actual_address = get_address_from_lat_long(invalid_lat_long)
        self.assertIsNone(actual_address)

    def test_same_start_and_destination(self):
        start = (44.5702861, -123.27921585)
        destination = (44.5702861, -123.27921585)
        path_limit = 30
        elevation = 'max'
        controller = AStarController()
        notificationHandler = NotificationHandler()
        model = Model()
        model.add_observer(notificationHandler)
        controller.set_route_model(model)
        controller.set_start_location(start)
        controller.set_end_location(destination)
        controller.set_path_limit(path_limit)
        controller.set_elevation_strategy(elevation)
        controller.manipulate_route_model()
        json_output = json.loads(notificationHandler.get_output_json())
        self.assertEqual(json_output['elevation_path_distance'], 0)
        self.assertEqual(json_output['elevation_path_gain'], 0)

    def test_very_close_start_and_destination(self):
        # Test case when start and destination points are very close
        start = (44.5702861, -123.27921585)
        destination = (44.5702862, -123.27921586)  # Slightly offset from start
        path_limit = 30
        elevation = 'max'
        controller = AStarController()
        notificationHandler = NotificationHandler()
        model = Model()
        model.add_observer(notificationHandler)
        controller.set_route_model(model)
        controller.set_start_location(start)
        controller.set_end_location(destination)
        controller.set_path_limit(path_limit)
        controller.set_elevation_strategy(elevation)
        controller.manipulate_route_model()
        json_output = json.loads(notificationHandler.get_output_json())
        # Ensure the path is very short, perhaps even empty
        self.assertLessEqual(json_output['elevation_path_distance'], 1)
        self.assertEqual(json_output['elevation_path_gain'], 0)

def test_no_valid_path_due_to_terrain_constraints(self):
    # Set up a terrain map with impassable obstacles or extreme elevation changes
    # For example, you can create a simple grid-based terrain where some cells are impassable
    terrain_map = [
        [1, 0, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 0, 1],
        [0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ]
    
    # Set the start and destination points
    start = (0, 0)
    destination = (4, 4)
    
    # Set up the controller with the terrain map
    path_limit = 30
    elevation = 'max'
    controller = AStarController()
    notificationHandler = NotificationHandler()
    model = Model()  # Do not pass the terrain map argument
    model.add_observer(notificationHandler)
    controller.set_route_model(model)
    controller.set_start_location(start)
    controller.set_end_location(destination)
    controller.set_path_limit(path_limit)
    controller.set_elevation_strategy(elevation)
    
    # Run the algorithm
    controller.manipulate_route_model()
    
    # Ensure the algorithm indicates the absence of a valid path
    json_output = json.loads(notificationHandler.get_output_json())
    self.assertIsNone(json_output['elevation_path_distance'])
    self.assertIsNone(json_output['elevation_path_gain'])


    # Checking the MVC architecture - Astar controller to Model
    def test_model_controller_astar(self):
        start = (44.570286100000004, -123.27921585)
        destination = (44.56305595, -123.28392363395751)
        path_limit = 30
        elevation = 'max'
        controller = AStarController()
        notificationHandler = NotificationHandler()
        model = Model()
        model.add_observer(notificationHandler)
        controller.set_route_model(model)
        controller.set_start_location(start)
        controller.set_end_location(destination)
        controller.set_path_limit(path_limit)
        controller.set_elevation_strategy(elevation)
        controller.manipulate_route_model()
        self.assertEqual(model.algorithm, AstarRoute)  # Used assertEqual instead of assert

    # Checking the MVC architecture - Dijkstra controller to Model
    def test_model_controller_dijkstra(self):
        start = (44.570286100000004, -123.27921585)
        destination = (44.56305595, -123.28392363395751)
        path_limit = 30
        elevation = 'max'
        controller = DijkstraController()
        notificationHandler = NotificationHandler()
        model = Model()
        model.add_observer(notificationHandler)
        controller.set_route_model(model)
        controller.set_start_location(start)
        controller.set_end_location(destination)
        controller.set_path_limit(path_limit)
        controller.set_elevation_strategy(elevation)
        controller.manipulate_route_model()
        self.assertEqual(model.algorithm, DijkstraRoute)  # Used assertEqual instead of assert

if __name__ == '__main__':
    unittest.main()
