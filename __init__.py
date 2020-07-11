from flask import Flask

import main

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world!"

@app.route('/search/<name>')
def search(name):
   return main.search_book(name)

@app.route('/locate/<book>')
def locate(book):
   return main.get_holding(book)

if __name__ == "__main__":
    app.run(debug=True)
