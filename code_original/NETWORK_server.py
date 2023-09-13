import time
from flask import Flask, request
from flask_restful import Resource, Api
from gevent.pywsgi import WSGIServer
import os
import platform

bar = ''
if platform.system() == "Linux":
    bar = "/"
elif platform.system() == "Windows":
    bar = '\\'

app = Flask(__name__)
api = Api(app)
data_directory = str(os.getcwd()) + bar + "network_data"

header="Time,Protocol,SourceIP,SourcePort,DestIP,DestPort,Length\n"

class sensor(Resource):

    def post(self, sensorid):
        vector = request.data.decode("utf-8")
        #print(vector)
        #vector = vector[:-1]
        vector = vector + "\n"
        file_path = data_directory + bar + sensorid
        append_write = 'a'  # append if already exists
        if not os.path.exists(file_path):
            file = open(file_path, append_write)
            file.write(header)
            file.close()
        file = open(file_path, append_write)
        file.write(vector)
        file.close()

        return 200


def launch_REST_Server():
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    api.add_resource(sensor, '/sensor/<sensorid>')  # Route_1
    http_server = WSGIServer(('0.0.0.0', 5002), app, certfile="tls.crt",keyfile="tls.key")
    http_server.serve_forever()


if __name__ == "__main__":
    launch_REST_Server()

