from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world!"


def test():
   return "test"
app.add_url_rule("/test", "test", test)

if __name__ == "__main__":
    app.run(debug=True)
