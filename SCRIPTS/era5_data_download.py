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

def get_pres_data(data,client):
    '''
    Downloads the pressure level data as a grib file by day.
    
    '''
    collection_id = 'reanalysis-era5-pressure-levels'
    
    request = {
            "product_type": ["reanalysis"],
            "variable": [
                "geopotential",
                "relative_humidity",
                "specific_humidity",
                "temperature",
                "u_component_of_wind",
                "v_component_of_wind"
            ],
            "year": data["year"],
            "month": data["month"],
            "day": data["day"],
            "time": data["time"],
            "data_format": data["data_format"],
            "download_format": "unarchived",
            "area": data["area"]
            }       
    filename = f"pres_data_{data["year"]}.grib"
    filename = os.path.join(data["download_folder"],filename)
    
    client.retrieve(collection_id, request, target=filename)    

def get_surf_data(data,client):
    '''
    Downloads the surface data as a grib file by day.
    '''
    collection_id = 'reanalysis-era5-single-levels'
    
    request = {
            "product_type": ["reanalysis"],
            "variable": [
                "10m_u_component_of_wind",
                "10m_v_component_of_wind",
                "2m_dewpoint_temperature",
                "2m_temperature",
                "land_sea_mask",
                "mean_sea_level_pressure",
                "sea_ice_cover",
                "sea_surface_temperature",
                "skin_temperature",
                "snow_depth",
                "soil_temperature_level_1",
                "soil_temperature_level_2",
                "soil_temperature_level_3",
                "soil_temperature_level_4",
                "surface_pressure",
                "volumetric_soil_water_layer_1",
                "volumetric_soil_water_layer_2",
                "volumetric_soil_water_layer_3",
                "volumetric_soil_water_layer_4",
                "total_cloud_cover",
                "total_precipitation",
                "surface_latent_heat_flux",
                "top_net_solar_radiation_clear_sky",
                "temperature_of_snow_layer",
                "soil_type",
                "leaf_area_index_high_vegetation"
            ],
            "year": data["year"],
            "month": data["month"],
            "day": data["day"],
            "time": data["time"],
            "data_format": data["data_format"],
            "download_format": "unarchived",
            "area": data["area"]
            }       
    
    filename = f"surf_data_{data["year"]}.grib"
    filename = os.path.join(data["download_folder"],filename)
        
    client.retrieve(collection_id, request, target=filename)

def main():
    if len(sys.argv) < 2:
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
    folder = os.path.abspath(data["download_folder"])
    folder = Path(folder)
    data["download_folder"] = folder

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