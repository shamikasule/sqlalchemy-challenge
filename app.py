import numpy as np
import datetime as dt

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
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start><br/>"
           
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session (link) from Python to the DB
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
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query
    stations=session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    result = list(np.ravel(stations))

    return jsonify(result)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create session (link) from Python to the DB
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

@app.route("/api/v1.0/start/<start_date>")
def startdate(start_date):
    
    #test to return date
    #d={"date":start_date}
    
    #return jsonify(d)

    session = Session(engine)
    
    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    
    min_date = session.query(Measurement.date).order_by(Measurement.date.asc()).first()
    
    mx_dt = dt.datetime.strptime(max_date[0], '%Y-%m-%d')
    mi_dt = dt.datetime.strptime(min_date[0], '%Y-%m-%d')
    str_dt = dt.datetime.strptime(start_date,'%Y-%m-%d')
    #mx_dt = dt.datetime.strptime(max_date[0], '%Y-%M-%d')
    #return jsonify(max_date)
    #return jsonify({"db":max_date[0],"conv":mx_dt})
    
    if str_dt <= mx_dt and str_dt >= mi_dt:
        return jsonify ({"yay!": f"The date {start_date} entered by the user exists in database."})
    else:
        return jsonify ({"error": f"The date {start_date} entered by the user does not exist in database."}), 404
    
    #for date in Measurement:
        #search_term = character["real_name"].replace(" ", "").lower()

        #if search_term == canonicalized:
            #return jsonify(character)
    
    # Query
    
    
    #canonicalized = real_name.replace(" ", "").lower()
    #query_date = dt.date(start_date) - dt.timedelta(days=365)
        
if __name__ == '__main__':
    app.run(debug=True)
