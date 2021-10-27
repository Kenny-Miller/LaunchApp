from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():

  # Todo: Implement backend

  obj = {
    "key": "val"
  }
  return obj
