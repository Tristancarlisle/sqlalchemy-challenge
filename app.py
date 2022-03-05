import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start-date<br/>"
        f"/api/v1.0/start-date/end-date<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
    
    date_prcp = []
    for date, prcp in results:
        date_prcp_dict = {}
        date_prcp_dict["Date"] = date
        date_prcp_dict["Precipitation"] = prcp
        
        date_prcp.append(date_prcp_dict)

    return jsonify(date_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()
    
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Measurement.tobs).filter(Measurement.date >= '2016-08-23',Measurement.station == 'USC00519281').all()

    session.close()

    # Convert list of tuples into normal list
    all_temps= list(np.ravel(results))

    return jsonify(all_temps)



@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all passenger names"""
    # Query all passengers
    mini = session.query(func.min(Measurement.tobs)).filter(Measurement.station == 'USC00519281', Measurement.date >= start).all()
    maxi = session.query(func.max(Measurement.tobs)).filter(Measurement.station == 'USC00519281', Measurement.date >= start).all()
    avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.station == 'USC00519281', Measurement.date >= start).all()

    session.close()


    out = []
    out.append(f'Minimum: {mini}')
    out.append(f'Maximum: {maxi}')
    out.append(f'Average: {avg}')

    out1= list(np.ravel(out))
    return jsonify(out1)

@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    min = session.query(func.min(Measurement.tobs)).filter(Measurement.station == 'USC00519281', Measurement.date >= start, Measurement.date <= end).all()
    max = session.query(func.max(Measurement.tobs)).filter(Measurement.station == 'USC00519281', Measurement.date >= start, Measurement.date <= end).all()
    avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.station == 'USC00519281', Measurement.date >= start, Measurement.date <= end).all()

    session.close()
    
    out = []
    out.append(f'Minimum: {min}')
    out.append(f'Maximum: {max}')
    out.append(f'Average: {avg}')

    out1= list(np.ravel(out))
    return jsonify(out1)





if __name__ == '__main__':
    app.run(debug=True)
