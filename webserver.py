#!/usr/bin/python3
from flask import Flask

app = Flask(__name__)
@app.route("/")
def index():
	with open('index.html') as f: s = f.read()
	return f	
	
def weather_log():
	return "FALSE"
