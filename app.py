from flask import Flask, jsonify

import datetime as dt
import numpy as np
import pandas as pd
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Access the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect database into our classes
Base = automap_base()

#reflect the database
Base.prepare(engine, reflect=True)

#Create a variable for each of the classes
Measurement = Base.classes.Measurement
Station = Base.classes.Station

# Create session link from Python to our database
session = Session(engine)

os.environ['PYTHONPATH'] = os.getcwd()

# define Flask app
app = Flask(__name__)

# Define the welcome route
@app.route("/")

# Set up routing information
def welcome():
    return(
        '''
        Welcome to the Climate Analysis API!
        Available Routes:
        /api/v1.0/precipitation
        /api/v1.0/stations
        /api/v1.0/tobs
        /api/v1.0/temp/start/end
        ''')

