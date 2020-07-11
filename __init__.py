from flask import Flask

import main

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world!"

@app.route('/search/<name>')
def search(name):
   return main.search(name)

if __name__ == "__main__":
    app.run(debug=True)
