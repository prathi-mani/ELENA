import json

ELEMENT = "ELEMENT"
STRING = "LineString"
METADATA = "metadata"
SHAPE = "shape"
CATEGORY_TYPE = "categoryType"
DATA_POINTS = "data_points"
ELEVATION_PATH = "path_elevation"
SHORTEST_PATH = "path_shortest"
SHORTEST_DIST = "shortest_distance"
SHORTEST_GAIN = "shortest_elevation_gain"
SHORTEST_DROP = "shortest_elevation_drop"
INITIAL_LOCATION = "start_location"
DESTINATION_LOCATION = "end_location"
ELEV_DIST = "elevation_path_distance"
ELEV_GAIN = "elevation_path_gain"
ELEV_DROP = "elevation_path_drop"
BOOL_FLAG = "boolean_flag"

def create_route_json(coordinates):
    route_json = {METADATA: {}, SHAPE: {}, CATEGORY_TYPE: ELEMENT}
    route_json[SHAPE][CATEGORY_TYPE] = STRING
    route_json[SHAPE][DATA_POINTS] = coordinates
    return route_json

class NotificationHandler:
    def __init__(self):
        self.output_data = {}

    def notify_route_update(self, optimal_route=None, elevation_route=None, initial_location=None, destination_location=None):
        print("elevation_route is ", elevation_route.algoName)
        self.output_data = {ELEVATION_PATH: create_route_json(elevation_route.path),
                            SHORTEST_PATH: create_route_json(optimal_route.path),
                            SHORTEST_DIST: optimal_route.distance, 
                            SHORTEST_GAIN: optimal_route.altitude_gain,
                            SHORTEST_DROP: optimal_route.altitude_drop, 
                            INITIAL_LOCATION: initial_location, 
                            DESTINATION_LOCATION: destination_location,
                            ELEV_DIST: elevation_route.distance, 
                            ELEV_GAIN: elevation_route.altitude_gain, 
                            ELEV_DROP: elevation_route.altitude_drop}
        
        if len(elevation_route.path) == 0:
            self.output_data[BOOL_FLAG] = 1
        else:
            self.output_data[BOOL_FLAG] = 2

    def get_output_json(self):
        print('Elevation Output Paths: ', self.output_data)
        return json.dumps(self.output_data)
