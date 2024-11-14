import json
import sys
#sys.path.insert(0, "/Users/prathim/Documents/SE/new-code/EleNa-project/src")

import googlemaps
from flask import Flask, request, render_template
from server.controller.AlgoController import *
from server.model.Model import *
from server.controller.NotificationHandler import NotificationHandler
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/get_elena_path": {"origins": "http://localhost:3000"}})
CORS(app)

@app.route('/')
def hello_world():
    return 'Developers EleNa Server'

@app.route('/get_elena_path', methods=['POST'])
def get_routes_via_address():
    json_output = request.get_json(force=True)
    start_address = json_output['origin_location']
    end_address = json_output['destination_location']
    origin_point = tuple(start_address)
    destination_point = tuple(end_address)
    path_limit = float(json_output['path_limit'])
    elevation_strategy = json_output['elevation_option']
    algorithm = json_output['selected_algorithm']
    model = Model()
    view = NotificationHandler()
    model.add_observer(view)
    if algorithm == "AStar":
        controller = AStarController()
    else:
        controller = DijkstraController()
    controller.set_route_model(model)
    controller.set_start_location(origin_point)
    controller.set_end_location(destination_point)
    controller.set_path_limit(path_limit)
    controller.set_elevation_strategy(elevation_strategy)
    controller.manipulate_route_model()
    output = view.get_output_json()
    # Since we do not have pre selected point markers on map, we need to add them manually
    # output["start"], output["end"] = origin_point[::-1], destination_point[::-1]
    return output
