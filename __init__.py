from flask import Flask, render_template
import json

import main

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/search/<name>')
def search(name):
   return json.dumps(main.search_book(name))

@app.route('/locate/<book>')
def locate(book):
   return json.dumps(main.get_holding(book))

if __name__ == "__main__":
    app.run(debug=True)
