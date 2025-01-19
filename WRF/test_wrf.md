# Running a Test Case in WRF

Next step is running a test to validate the WRF installation.

```bash
wget https://ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.20240528/00/atmos/gfs.t00z.pgrb2.0p25.f000
wget https://ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.20240528/00/atmos/gfs.t00z.pgrb2.0p25.f003
wget https://ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.20240528/00/atmos/gfs.t00z.pgrb2.0p25.f006
wget https://ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.20240528/00/atmos/gfs.t00z.pgrb2.0p25.f009
wget https://ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.20240528/00/atmos/gfs.t00z.pgrb2.0p25.f012
```

time-independent error - try using binary format, not cdf

**Download url**
```bash
url="https://www2.mmm.ucar.edu/wrf/src/wps_files/geog_high_res_mandatory.tar.gz"
```
**Downloading the WPS GEOG Data**
```bash
wget ${url}
```
unzipping and untaring the downloaded WPS GEOG tar file
```bash
gunzip geog_high_res_mandatory.tar.gz
tar -xvf geog_high_res_mandatory.tar WPS_GEOG
```