from flask import Flask

import Main

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world!"

@app.route('/search/<name>')
def search(name):
   return Main.search(name)

if __name__ == "__main__":
    app.run(debug=True)
