# Using ERA% for WRF

This document covers downloading, preprocessing and running WRF using ERA5 data.

## Contents
- [Using ERA% for WRF](#using-era-for-wrf)
  - [Contents](#contents)
  - [Downloading ERA5 Reanalysis](#downloading-era5-reanalysis)
  - [Preprocessing](#preprocessing)
    - [GEOGRID](#geogrid)
  - [Running WRF](#running-wrf)

## Downloading ERA5 Reanalysis

The first step is to download surface and pressure level data from the Climate Data Store. See python script for an example of downloading.

Download each as a separate file. You can download multiple files if needed such as by day.



## Preprocessing

This section covers using WPS to preprocess the ERA5 data.

If you haven't already, you need to get the Static Geographic Data that GEOGRID requires to run.


### GEOGRID

Geogrid interpolates all of the terrestrial boundary conditions for the domain. This must be run first. It only needs to be run once for a domain.

geogrid

If geogrid hangs on GREENFRAC then we need to remove the search option from interpolation

open GEOGRID.TBL - around lines 149 or so you'll see the name=GREENFRAC

there are four lines that start with interp_option - at the end of these lines is a +search, remove that


Ungribbing the data you downloaded from ERA5 is a two step process. You have to ungrib both the surface data and then the levels data. 

ungrib

link sruface era file as a GRIBFILE.AAA
run ungrib

delete gthe GRIBFILE

link levels era file as a GRIBFILE.AAA
ungrib

then run metgrid


## Running WRF

make sure levels # in namelist.input are equal to or less than the number of levels in the era data

p_top must be less than or equal to the highest level in the era data


you must run real with regular WRF, the real.exe after compiling polar WRF is broken and does not write p_top to the wrfinput_d01 file

you can accomplish this in your batch submit scripts by calling the different environments and running the executables


