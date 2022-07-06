from flask import Flask
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello this code was updated by magic 2.0"