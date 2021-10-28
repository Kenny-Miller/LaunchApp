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

@app.route("/launchApp", methods=['Post'])
def start_app():
  data = request.get_json()
  print(data)

  #Todo start app on each machine

  return "", 200