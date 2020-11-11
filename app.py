import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
#################################################
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the measurement & station tables
Measurement = Base.classes.measurement

Station = Base.classes.station

# Flask Setup
#################################################

app = Flask(__name__)

# Flask Routes
#################################################

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return ("Welcome to Climate App!<br/>"
        f"The following routes are available:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    sel = [Measurement.date, func.avg(Measurement.prcp)]
    year_range=session.query(*sel).\
    filter(Measurement.date.between("2016-08-23", "2017-08-23")).\
    group_by(Measurement.date).all()
    year_range

    session.close()

    # Convert list of tuples into normal list
    result = list(np.ravel(year_range))

    return jsonify(result)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    stations=session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    result = list(np.ravel(stations))

    return jsonify(result)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    sel = [Measurement.date, Measurement.tobs]
    temp_range=session.query(*sel).\
    filter(Measurement.station == 'USC00519281').\
    filter(func.strftime("%Y", Measurement.date) == "2017").\
    order_by(Measurement.tobs.desc()).all()
    temp_range

    session.close()

    # Convert list of tuples into normal list
    result = list(np.ravel(temp_range))

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)