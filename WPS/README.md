# WPS Basics

WPS or WRF Preprossing System is used to get all of the necessary boundary and initial condition data in the right format for WRF and MPAS. This includes geographic data like soil information, meteorlogicla data like ERA5 or GFS data on surface and pressure levels, etc.

## WPS Workflow Overview

The general steps for preprocessing your data

### Creating A Domain

Use the domain wizard.
https://wrfdomainwizard.net/

### Get Geog Data

download and decompress geog data for geogrid

### Running GeoGrid

Geogrid to process your terrain data.

salloc --partition=regc
source env_script

In wps_job folder
Edit namelist
geog_data_path -> ../data/WPS_GEOG

run geogrid.exe


### Ungribbing Your Data

This step takes your GRIB data and unpacks it into an intermediate format.

You'll have to run ungrib twice for ERA5 data, once for the pressure level files and again for the surface data files.

Link the pressure files to GRIBFILE.AAAs, set the namelist file identifier and run ungrib

Repeat for the furface files, changing the namelist file identifier to match the surface files

### Running Metgrid

Interpolating your boundary and initial conditions for WRF



