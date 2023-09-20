import time
from flask import Flask, request
from flask_restful import Resource, Api
from gevent.pywsgi import WSGIServer
import os
import platform
import csv

bar = ''
if platform.system() == "Linux":
    bar = "/"
elif platform.system() == "Windows":
    bar = '\\'

app = Flask(__name__)
api = Api(app)
data_directory = str(os.getcwd()) + bar + "entropy_data"

class sensor(Resource):

    def post(self, sensorid):
        vector = request.data.decode("utf-8")

        vector = vector + "\n"
        file_path = data_directory + bar + "{}.txt".format(sensorid)
        
        # Check if the file exists, and if not, create it with headers
        if not os.path.exists(file_path):
            os.system(r"touch {}".format(sensorid))

        # Append the data to the file
        file = open(file_path, "a")
        file.write(vector)
        file.close()


def launch_REST_Server():
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    api.add_resource(sensor, '/sensor/<sensorid>')  # Route_1
    http_server = WSGIServer(('0.0.0.0', 5002), app)
    http_server.serve_forever()

if __name__ == "__main__":
    launch_REST_Server()

