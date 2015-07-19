#!/usr/bin/python3
from flask import Flask
import main
import json

wxc = main.WXConnector()

app = Flask(__name__)
@app.route("/")
def hello():
	with open('index.html') as f: s = f.read()
	return s	

@app.route("/data/<ziplist>")	
def weather_log(ziplist):
	rval=[]
	ziplist=ziplist.split(",")
	wxc.db_connect()
	for zip in ziplist:
		temps=wxc.getlast_20_temp(zip);
		row={'name': zip, 'data': temps}
		rval.append(row)
	return json.dumps({'series': rval})

app.debug = True	
app.run()
