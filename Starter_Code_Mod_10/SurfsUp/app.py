# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Starter_Code_Mod_10/SurfsUp/Resources/hawaii.sqlite")
Base = automap_base()

# Reflect an existing database into a new model
Base.prepare(engine, reflect=True)

# Reflect the tables
Measurements = Base.classes.measurement
Stations = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session (link) from Python to the DB
    session = Session(engine)
    # Query to retrieve the last 12 months of precipitation data
    results = session.query(Measurements.date, Measurements.prcp).order_by(Measurements.date).all()
    session.close()

    # Convert to list of dictionaries to jsonify
    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    # Create session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Stations.station).all()
    session.close()

    # Convert query results to a list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create session (link) from Python to the DB
    session = Session(engine)
    # Query the dates and temperature observations of the most active station for the last year
    most_active_station = 'USC00519281'
    results = session.query(Measurements.date, Measurements.tobs).filter(Measurements.station == most_active_station).order_by(Measurements.date).all()
    session.close()

    # Convert query results to a list of dictionaries
    tobs_data = list(np.ravel(results))

    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def temp_stats_start(start):
    #Return a JSON list of the minimum temperature, the average temperature, 
    #and the maximum temperature for a specified start or start-end range.
    
    # Create session (link) from Python to the DB
    session = Session(engine)
    
    # Query for the data
    results = session.query(
                func.min(Measurements.tobs), 
                func.avg(Measurements.tobs), 
                func.max(Measurements.tobs)
              ).filter(Measurements.date >= start).all()
    session.close()
    
    # Create a dictionary to hold the results
    temps = list(np.ravel(results))
    
    # Return the JSON representation of the dictionary
    return jsonify(temps=temps)

@app.route("/api/v1.0/<start>/<end>")
def temp_stats_start_end(start, end):
    #Return a JSON list of the minimum temperature, the average temperature, 
    #and the maximum temperature for a specified start or start-end range.
    
    # Create session (link) from Python to the DB
    session = Session(engine)
    
    # Query for the data
    results = session.query(
                func.min(Measurements.tobs), 
                func.avg(Measurements.tobs), 
                func.max(Measurements.tobs)
              ).filter(Measurements.date >= start, Measurements.date <= end).all()
    session.close()
    
    # Create a dictionary to hold the results
    temps = list(np.ravel(results))
    
    # Return the JSON representation of the dictionary
    return jsonify(temps=temps)

if __name__ == '__main__':
    app.run(debug=True)
