import time
import threading
from flask import Flask, request
from flask_restful import Resource, Api
from gevent.pywsgi import WSGIServer
import os
import platform
from ssl import SSLEOFError
from gevent.pywsgi import WSGIServer
import traceback

bar = ''
if platform.system() == "Linux":
    bar = "/"
elif platform.system() == "Windows":
    bar = '\\'

app = Flask(__name__)
api = Api(app)
data_directory = str(os.getcwd()) + bar + "device1/Bashlite/network_data"

header = "Time,Protocol,SourceIP,SourcePort,DestIP,DestPort,Length\n"


class sensor(Resource):

    def post(self, sensorid):
        vector = request.data.decode("utf-8")
        vector += "\n"
        file_path = os.path.join(data_directory, "net.csv")
        append_write = 'a'

        with open(file_path, append_write) as file:
            if os.path.getsize(file_path) == 0:  # Check if file is empty
                file.write(header)
            file.write(vector)

        return 200
        
        
        
class CustomWSGIServer(WSGIServer):

    def handle_error(self, type, value, tb):
        # Print the error
        traceback.print_exception(type, value, tb)
        # Restart the server (by raising the exception further)
        raise value


def force_restart():
    """Thread routine to trigger a server restart every 60 seconds."""
    while True:
        time.sleep(60)
        raise Exception("Scheduled restart after 1 minute.")


def launch_REST_Server():

    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    api.add_resource(sensor, '/sensor/<sensorid>')  # Route_1

    # Start the force_restart thread
    threading.Thread(target=force_restart).start()

    while True:  # This will ensure the server tries to restart upon an exception
        try:
            http_server = CustomWSGIServer(('0.0.0.0', 5002), app, certfile="tls.crt", keyfile="tls.key")
            http_server.serve_forever()
        except Exception as e:
            print(f"Unexpected error occurred: {e}. Restarting server...")
            time.sleep(5)  # Give it a 5-second delay before restarting

if __name__ == "__main__":
    launch_REST_Server()

