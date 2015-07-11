#!/usr/bin/python3
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import pywapi
import string
import pprint 
import json 
import sqlite3

__author__ = "josh"
__date__ = "$Jun 27, 2015 8:30:40 PM$"


class WXConnector:
    conn = 0
    cur = 0

    def db_connect(this):
        this.conn = sqlite3.connect('weather.db')
        this.cur = this.conn.cursor();
        this.cur.execute("CREATE TABLE IF NOT EXISTS weather (zip INTEGER, temp REAL, humidity REAL, pressure REAL, windspeed REAL, direction INTEGER, time DATETIME DEFAULT CURRENT_TIMESTAMP)")

    def save_wx(this, zipcode, temp, humidity, pressure, windspeed, direction):
        param=(zipcode,temp,humidity,pressure,windspeed,direction)
        query="INSERT INTO WEATHER (zip, temp, pressure, humidity,windspeed, direction) VALUES (?,?,?,?,?,?);"
        this.cur.execute(query,param)
        this.conn.commit()
        print("WX saved for {0:d}".format(zipcode))

    def load_temp(this, zipcode):
        yahoo = pywapi.get_weather_from_yahoo(str(zipcode))
        yd=json.dumps(yahoo)
        temp=yahoo["condition"]["temp"]    
        pressure=yahoo["atmosphere"]["pressure"]
        windspeed=yahoo["wind"]["speed"]
        direction=yahoo["wind"]["direction"]
        humidity=yahoo["atmosphere"]["humidity"]
        this.save_wx(zipcode,temp,humidity,pressure,windspeed,direction)

    def get_last(this, value, count,zip):
        #fields=(temp,humidity,pressure,windspeed,direction)
        query="SELECT time, %s FROM weather WHERE zip=? ORDER BY time DESC LIMIT ?" % value
        param=(zip,count);
        this.cur.execute(query,param)
        return this.cur.fetchmany(count)


    def __getattr__(this, name):
        def method(*args):
            parts=name.split("_",3)
            if parts[0] == "getlast":
                sa=this.get_last(parts[2], int(parts[1]),args[0])
                return sa
            else:
                print("Unknown method " + name)
        return method


if __name__ == "__main__":
    wxc = WXConnector()
    wxc.db_connect()
    wxc.load_temp(22041)
    wxc.load_temp(83715)
    x=wxc.getlast_20_temp(22041);
    print(x)
