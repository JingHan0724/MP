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
data_directory = str(os.getcwd()) + bar + "block_data"

fieldnames = ["datetime", "device", "read_ops", "write_ops", "read_kbs", "write_kbs", "avgrq_sz", "avg_queue", "await", "r_await", "w_await", "svctm", "util"]

class sensor(Resource):

    def post(self, sensorid):
        vector = request.data.decode("utf-8")
        
        # Vector should be a comma-separated string with data
        data = vector.split(',')

        file_path = data_directory + bar + "{}.csv".format(sensorid)
        
        # Check if the file exists, and if not, create it with headers
        if not os.path.exists(file_path):
            with open(file_path, "w") as csvfile:
                csv_write = csv.writer(csvfile)
                csv_write.writerow(fieldnames)

        # Append the data to the CSV file
        with open(file_path, "a") as csvfile:
            csv_write = csv.DictWriter(csvfile, fieldnames=fieldnames)
            data_dict = dict(zip(fieldnames, data))
            csv_write.writerow(data_dict)

def launch_REST_Server():
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    api.add_resource(sensor, '/sensor/<sensorid>')  # Route_1
    http_server = WSGIServer(('0.0.0.0', 5002), app)
    http_server.serve_forever()

if __name__ == "__main__":
    launch_REST_Server()

