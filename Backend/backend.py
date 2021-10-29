import socket
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/getApps", methods=['Get'])
def get_apps():

  apps = [
    "Sage2",
    "Panoptic"
  ]
  
  response = app.response_class(
    response=json.dumps(apps),
    status=200,
    mimetype='application/json'
  )
  return response

@app.route("/launchApp", methods=['Get'])
def start_app():
  #data = request.get_json()
  #print(data)

  HOST = '127.0.0.1'  # The server's hostname or IP address
  PORT = 65432        # The port used by the server

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
  #Todo start app on each machine

  return "", 200