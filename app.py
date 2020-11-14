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
        f"/api/v1.0/start/end/<start_date>/<end_date>"          
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
    
    #Create dictionary
    prcp_data = {}
    for row in year_range:
        #data = row[0]
        key = row[0]
        val = row[1]
        prcp_data[key]=val
  
    return jsonify(prcp_data)

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
    # Create session (link) from Python to the DB
    session = Session(engine)
    
    # Get max date from DB
    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    
    # Get min date from DB
    min_date = session.query(Measurement.date).order_by(Measurement.date.asc()).first()
    
    # Convert to date format
    mx_dt = dt.datetime.strptime(max_date[0], '%Y-%m-%d')
    mi_dt = dt.datetime.strptime(min_date[0], '%Y-%m-%d')
    str_dt = dt.datetime.strptime(start_date,'%Y-%m-%d')
    
    # Check to see if user enters a valid date in valid format-if yes,runs the calculation query-else returns error message
    if str_dt <= mx_dt and str_dt >= mi_dt:
        sel=[func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
        temp_range=session.query(*sel).\
        filter(Measurement.date >= start_date).\
        order_by(Measurement.date).all()
        temp_range
        
        session.close()
        
        # Convert list of tuples into normal list
        result=list(np.ravel(temp_range))
        
         #Create dictionary
    #temp_data ={}
    #temp_data["Min.Temp"] = []
    #temp_data["Max.Temp"]=[]
    #temp_data["Avg.Temp"]=[]
    #for Min.Temp, Max.Temp, Avg.Temp in temp_range:
        #temp_data["Min.Temp"] = [0][0]
        #temp_data["Max.Temp"] = [0][1]
        #temp_data["Avg.Temp"] = [0][2]
                          
        return jsonify (temp_data)
    else:
        return jsonify ({"error": f"The date {start_date} entered by the user does not exist in database."}), 404
    
@app.route("/api/v1.0/start/end/<start_date>/<end_date>")
def start_end_date(start_date,end_date):
   
    # Create session (link) from Python to the DB
    session = Session(engine)
         
    # Get max date from DB
    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    
    # Get min date from DB
    min_date = session.query(Measurement.date).order_by(Measurement.date.asc()).first()
    
    # Convert to date format
    mx_dt = dt.datetime.strptime(max_date[0], '%Y-%m-%d')
    mi_dt = dt.datetime.strptime(min_date[0], '%Y-%m-%d')
    str_dt = dt.datetime.strptime(start_date,'%Y-%m-%d')
    end_dt = dt.datetime.strptime(end_date,'%Y-%m-%d')
    
    if (str_dt <= mx_dt and str_dt >= mi_dt):
        sel=[func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
        temp_range=session.query(*sel).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).\
        order_by(Measurement.date).all()
        temp_range
        
        session.close()
       
        result=list(np.ravel(temp_range))
                    
        return jsonify (result)
    else:
        return jsonify ({"error": f"The date {start_date} entered by the user does not exist in database."}), 404
        
if __name__ == '__main__':
    app.run(debug=True)
