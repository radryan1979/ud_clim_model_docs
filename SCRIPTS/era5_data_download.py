#!/usr/bin/env python3

'''
This script downloads data for pressure levels and surface for WRF.

Creates and downloads requests for each day of your model run.

Use a JSON file with this structure to pass parameters:

{
    download_folder: '',
    area: [N,W,S,E],
    data_format: 
    year: '',
    month: ['01','02',...],
    day: ['01','02',...],
    time: ['00:00','03:00',...],
}

Requires the ECMWF client python package. See this link for more info:
https://cds.climate.copernicus.eu/how-to-api

'''

import sys
import os
import json
from pathlib import Path
from ecmwf.datastores import Client
import logging

logging.basicConfig(
    level="INFO",
    format="%(asctime)s ]%(levelname)s %(message)s"
    )

def get_pres_data(thedate,hours,download_folder,client):
    '''
    Downloads the pressure level data as a grib file by day.
    
    '''
    collection_id = 'reanalysis-era5-pressure-levels'
        

def get_surf_data(thedate,hours,download_folder,client):
    '''
    Downloads the surface data as a grib file by day.
    '''
    collection_id = 'reanalysis-era5-single-levels'

def main():
    if len(sys.argv) < 4:
        print("Usage: python script.py <JSON_file>")
        sys.exit(1)

    # Parse parameters
    json_file = sys.argv[1]

    try:
        with open(json_file) as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.info("File not found")
        sys.exit(74)
    except json.JSONDecodeError as e:
        logging.info(f"Invalid JSON: {e}")
        sys.exit(4)
    

    # Normalize folder path
    folder = os.path.abspath(data.download_folder)
    folder = Path(folder)
    data.download_folder = folder

    logging.info(f"Folder entered: {folder}")
    
    client = Client()
    
    try:
        client.check_authentication()
    except Exception as e:
        logging.info(f"An error occured authenticating to CDS. \n {e}")
        sys.exit(3)
    
    try:
        folder.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.info(f"An error occured trying to create the downloads folder. \n {e}")
        sys.exit(74)
    
    get_surf_data(data,client)
    get_pres_data(data,client)
    

if __name__ == "__main__":
    main()