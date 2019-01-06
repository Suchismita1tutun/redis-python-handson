#!/usr/bin/python
 
# Author  : Fajri Abdillah a.k.a clasense4
# Twitter : @clasense4
# mail    : clasense4@gmail.com
 
# import modules used here -- sys is a very standard one
import sys
from flask import Flask
import  mysql.connector
import redis # ==> Make sure to install this library using pip install redis
from datetime import datetime
import time
import _pickle as cPickle
import hashlib


app = Flask(__name__)
 
db = mysql.connector.Connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="root",  # your password
                     db="appDB")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
CURSOR = db.cursor()


# START TIME
startTime = datetime.now()

# Redis Object
R_SERVER = redis.Redis("localhost")
 
sql = "select * from user" # Or Any SQL script
TTL = 36 

@app.route("/api")
# Gather our code in a main() function
def cache_redis():
    # INPUT 1 : SQL query
    # INPUT 2 : Time To Life
    # OUTPUT  : Array of result
 
    # Create a hash key
    hash = hashlib.sha224(sql).hexdigest()
    key = "sql_cache:" + hash
    print("Created Key\t : %s" % key)
    
    # Check if data is in cache.
    if (R_SERVER.get(key)):
        print("This was return from redis")    
        return cPickle.loads(R_SERVER.get(key))
    else:
        # Do MySQL query   
        CURSOR.execute(sql)
        data = CURSOR.fetchall()
        
        # Put data into cache for 1 hour
        R_SERVER.set(key, cPickle.dumps(data) )
        R_SERVER.expire(key, TTL);
 
        print("Set data redis and return the data")
        return cPickle.loads(R_SERVER.get(key))
 
# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("8000"), debug=True)