class RouteInfo:
    def __init__(self):
        # Initialize the class variables
        self.algoName = "AStar"  # Algorithm name
        self.origin_location = None, None  # Origin location coordinates
        self.destination_location = None, None  # Destination location coordinates
        self.path = []  # Route path
        self.altitude_gain = 0  # Altitude gain
        self.altitude_drop = 0  # Altitude drop
        self.distance = 0.0  # Distance

