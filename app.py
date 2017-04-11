import json
import pprint
from config import *
import sys
import time
import json
import requests
import time
from flask import Flask, render_template, request
# import certifi


app = Flask(__name__)



@app.route("/")
def index():
	return "Hello"



if __name__ == "__main__":
    app.debug = True
    app.run(port=8000)
