import json
import Adafruit_DHT
from flask import Flask, render_template, request
import main

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/search', methods = ['GET'])
def search():
    return json.dumps(main.search_book(request.args.get('q')))

@app.route('/ids', methods = ['GET'])
def ids():
    return json.dumps(main.get_imagelinks(request.args.get('q').split(',')))

@app.route('/img', methods = ['GET'])
def locate():
    return json.dumps(main.get_holding(request.args.get('q')))

@app.route('/report', methods = ['GET'])
def report():
    return json.dumps(main.get_holdings(request.args.get('q').split(",")))

@app.route('/sensors', methods = ['GET'])
def sensor():
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    return json.dumps({'Temperature':temperature, 'Humidity':humidity})

if __name__ == "__main__":
    app.run(debug=True)
