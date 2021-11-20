from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/client")
def client():
    return render_template("client.html")

@app.route("/employee")
def client():
    return render_template("employee.html")



if __name__ == "__main__":
    app.run(debug = True)