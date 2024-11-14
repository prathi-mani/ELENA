import os
import pickle as pkl
import osmnx as ox
from haversine import haversine, Unit


class ModelManager:
    def __init__(self):
        self.graph = None
        self.map_key = "AIzaSyAemV5rJxDdllmy32bG_ua2x8RiUaSHU2Y"
        self.mid_point = (44.5646, -123.2620) # Centre point of Oregon State University, Corvallis
        self.offline_map_location = "../offlineStreetMap.p"

    def analyze_elevation_graph(self, target_loc):

        print("Loading the offline map....", self.offline_map_location)
        try:
            with open(self.offline_map_location, "rb") as file:
                self.graph = pkl.load(file)

            self.graph = ox.add_edge_grades(self.graph)
        except:
            if os.path.exists("../offlineStreetMap.p"):
                self.graph = pkl.load(open(self.offline_map_location, "rb"))
                self.graph = ox.add_edge_grades(self.graph)
            else:
                print("Offline map not found.")
                self.save_map_to_cache()
        target_location = self.graph.nodes[ox.distance.nearest_nodes(self.graph, target_loc[0], target_loc[1])]
        for node, data in self.graph.nodes(data=True):
            target_X = target_location['y']
            target_Y = target_location['x']
            target_loc_X = self.graph.nodes[node]['y']
            target_loc_Y = self.graph.nodes[node]['x']
            data['dist_from_dest'] = haversine((target_X, target_Y), (target_loc_X, target_loc_Y), unit=Unit.METERS)

        return self.graph
    
    def save_map_to_cache(self):
        print("Map is downloading...")
        self.graph = ox.graph_from_point(self.mid_point, dist=15000, network_type='walk')
        self.graph = ox.add_node_elevations_google(self.graph, api_key=self.map_key)
        pkl.dump(self.graph, open(self.offline_map_location, "wb"))
        print("Graph is saved for offline usage!")
