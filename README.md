# hh_fapi

The API layer for the Home Historian system, implemented in FastAPI. 

## Purpose
This project is being used to learn FastAPI, and API design patterns.

## What does it do?
Home Historian is a system for the collection of time-series data from around the home.  Initially the schema contains only sensors and their readings.

## How to run it?
* Install Python 3 and pip
* Update pip: `pip install --upgrade pip`
* Run the web server: `uvicorn app.main:app --reload`
