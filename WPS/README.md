# WPS Basics

WPS or WRF Preprossing System is used to get all of the necessary boundary and initial condition data in the right format for WRF and MPAS. This includes geographic data like soil information, meteorlogicla data like ERA5 or GFS data on surface and pressure levels, etc.

## WPS Workflow Overview

The general steps for preprocessing your data

### Creating A Domain

Use the domain wizard.
https://wrfdomainwizard.net/

### Running GeoGrid

Geogrid to process your terrain data.

### Ungribbing Your Data

This step takes your GRIB data and unpacks it into an intermediate format.

### Running Metgrid

Interpolating your boundary and initial conditions for WRF



