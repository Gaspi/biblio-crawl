from flask import Flask, render_template, request
import json

import main

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/search', methods = ['GET'])
def search():
    query = request.args.get('q')
    return json.dumps(main.search_book(query))

@app.route('/ids', methods = ['GET'])
def ids():
    query = request.args.get('q')
    return json.dumps(main.get_imagelinks(query.split(',')))

@app.route('/img', methods = ['GET'])
def locate():
    query = request.args.get('q')
    return json.dumps(main.get_holding(query))

@app.route('/report', methods = ['GET'])
def report():
    query = request.args.get('q')
    return json.dumps(main.get_holdings(query.split(",")))

if __name__ == "__main__":
    app.run(debug=True)
