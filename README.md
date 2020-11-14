# SQLAlchemy-challenge

> This challenge involves climate analysis & exploration of a climate database.
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Analysis](#analysis)

## General info
This is a SQLAlchemy data analysis & exploration project. A sqlite database that has hawai's stations data & precipitation & temperature
observations for a period of 2010 - 2017 is the input/resource file for analysis. Analysis is done using combination
of SQLAlchemy, ORM queries, pandas & Flask APIs. 

## Technologies
Project is created with:
* jupyter notebook - version 6.0.3

## Setup
To run this project, install or check installation of:
* SQLAlchemy
* Flask

## Analysis


### Precipitation Analysis:
 Initial steps of connecting to sqlite database, reflecting tables into classes & saving references to those classes done using SQLAlchemy.
* query to get most recent date in the db.
* used dt.timedelta to get date from a year ago from most recent date.
* designed a query to retrieve the dates & avg. precipitation scores.
* used between, to filter between two dates, to get the data for analysis.
* query results are saved as pandas df & plotted as bar chart.
* calculated summary statistics for precipitation data.

### Station Analysis:

* designed a query to get the count of stations in the dataset.
* designed query to list the most active stations with their counts in descending order.
* designed a query to get the min, max & avg temps for most active station.
* designed a query to get the last 12 months of tobs data for the most active station.
* query results are saved as pandas df & plotted as histogram.

### Climate App:
* created routes for home page listing all available routes. There are static & dynamic routes.
* for query to calculate avg.precipitation, converted the results to a dictionary with date as key & avg.precipitation values as value.
* for dynamic routes, added a conversion of date string to datetime to check if date is entered in valid format & to be able to check the date conditionals.
* converted the o/p list to dictionary.