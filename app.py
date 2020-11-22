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
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session link from Python to our database
session = Session(engine)

# os.environ['PYTHONPATH'] = os.getcwd()

# define Flask app
app = Flask(__name__)

# Define the welcome route
@app.route("/")

# Set up routing information
def welcome():
    return(
        '''
        Welcome to the Climate Analysis API!<br/>
        Available Routes:<br/>
        /api/v1.0/precipitation<br/>
        /api/v1.0/stations<br/>
        /api/v1.0/tobs<br/>
        /api/v1.0/temp/start/end
        ''')
# Define precipitation route
@app.route("/api/v1.0/precipitation")

#Create precipitation function
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
       filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

#Define station route
@app.route("/api/v1.0/stations")

# Define station function
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#Define temperature route
@app.route("/api/v1.0/tobs")

# Define temp function
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Create routes for statistical analysis
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# Define function
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
