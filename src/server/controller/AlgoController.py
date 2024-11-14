
from server.model.Algorithms import AstarRoute, DijkstraRoute

class RouteController():
    def __init__(self):
        super().__init__()
        self.route_model = None
        self.observer = None
        self.elevation_strategy = None
        self.start_location = None
        self.end_location = None
        self.path_limit = None

    def set_route_model(self, route_model):
        self.route_model = route_model

    def set_elevation_strategy(self, elevation_strategy):
        self.elevation_strategy = elevation_strategy

    def set_start_location(self, start_location):
        self.start_location = start_location

    def set_end_location(self, end_location):
        self.end_location = end_location

    def set_path_limit(self, path_limit):
        self.path_limit = path_limit

    def manipulate_route_model(self):
        # This method will be overridden by subclasses to specify the routing algorithm.
        raise NotImplementedError("This method should be overridden by subclasses.")

class AStarController(RouteController):
    def manipulate_route_model(self):
        self.route_model.update_algorithm(AstarRoute)
        self.route_model.compute_paths(self.start_location, self.end_location, self.path_limit, self.elevation_strategy)

class DijkstraController(RouteController):
    def manipulate_route_model(self):
        self.route_model.update_algorithm(DijkstraRoute)
        self.route_model.compute_paths(self.start_location, self.end_location, self.path_limit, self.elevation_strategy)
