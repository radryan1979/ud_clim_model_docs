# Polar WRF Installation on Caviness

This document will walk you through compiling polar WRF on the Caviness cluster.

## Prerequisite

Before following the steps to compile Polar WRF, you must first compile and install regular WRF. See instructions here. Once you've done that, you'll replace some of the source files in the regular WRF folders with Polar WRF source files and then recompile your WRF build.

You'll also want to make sure that you've compiled and installed the WRF version that matches the Polar WRF version you plan to install. These instructions are for Polar WRF 4.5, thus you'll want to have a WRF 4.5 clean build.

Note that each version of Polar WRF has some differences in the source files that need to be copied and so you'll want to manually go through the Polar WRF source to identify each file that will replace a WRF source file.

### Obtain Polar WRF Files

You can grab the zip file for a given version of Polar WRF from the Clouds, Wind, and Climate Lab Google drive folder [here](https://drive.google.com/drive/folders/1_m-YOaccorMXx4vJPlf2jT6lcpQCM7Mt?usp=share_link). Once you have the zip, you can use `scp` to secure copy the file from your local machine to Caviness.

### Login and Workgroup

Once you've logged into Caviness, the first step is to set your workgroup. Remember to do this everytime you log in.

`workgroup -g regc`

### Caviness OpenMPI

You'll need to make sure you activate the OpenMPI package on Caviness before you begin, otherwise you will not be able to compile and/or run WRF.

```bash
vpkg_require openmpi/4.0.2:intel
```

### Set Your Environment Variables

You'll want to make sure you've set all of your environment variables in the same way as outlined in the WRF installation instructions as you'll be recompiling and reinstalling WRF once you've copied the Polar WRF source files in.

## Replace WRF Source Files

The first step is to replace some of the source files in the WRF folders with the Polar WRF source files. **Each version of Polar WRF is different!** The script below is specifically for Polar WRF / WRF 4.5. If you are using a previous version, please thoroughly go through the Polar WRF folders and edit the script below to copy / replace the files listed in the Polar WRF source folders.

You can copy and paste this script then update the folders and run it:

```bash
#!/usr/bin/env bash

# This script is for Polar WRF 4.5

# Please update the following folder locations to match your setup
# pwrf_src is the location of the unzipped Polar WRF files
# wrf_src is your compiled WRF installation that you'll be converting to Polar WRF
# wps_src is as above also

pwrf_src="/work/regc/polarWRF/pwrf455/src/pWRF_4_5_1"
wrf_src="/work/regc/polarWRF/pwrf455/src/WRF"
wps_src="/work/regc/polarWRF/pwrf455/src/WPS"

#Copy the polar WRF files into the WRF directory

pwd
echo "Moving files..."

# dyn_em folder
mv "${wrf_src}/dyn_em/module_first_rk_step_part1.F" "${wrf_src}/dyn_em/module_first_rk_step_part1.F-unpolar"
mv "${wrf_src}/dyn_em/module_initialize_real.F" "${wrf_src}/dyn_em/module_initialize_real.F-unpolar"

#phys folder
mv "${wrf_src}/phys/module_mp_morr_two_moment.F" "${wrf_src}/phys/module_mp_morr_two_moment.F-unpolar"
mv "${wrf_src}/phys/module_mp_p3.F" "${wrf_src}/phys/module_mp_p3.F-unpolar"
mv "${wrf_src}/phys/module_mp_thompson.F" "${wrf_src}/phys/module_mp_thompson.F-unpolar"

mv "${wrf_src}/phys/module_sf_noah_seaice_drv.F" "${wrf_src}/phys/module_sf_noah_seaice_drv.F-unpolar"
mv "${wrf_src}/phys/module_sf_noah_seaice.F" "${wrf_src}/phys/module_sf_noah_seaice.F-unpolar"

mv "${wrf_src}/phys/module_sf_noahdrv.F" "${wrf_src}/phys/module_sf_noahdrv.F-unpolar"
mv "${wrf_src}/phys/module_sf_noahlsm_glacial_only.F" "${wrf_src}/phys/module_sf_noahlsm_glacial_only.F-unpolar"
mv "${wrf_src}/phys/module_sf_noahlsm.F" "${wrf_src}/phys/module_sf_noahlsm.F-unpolar"

mv "${wrf_src}/phys/module_sf_noahmp_glacier.F" "${wrf_src}/phys/module_sf_noahmp_glacier.F-unpolar"
mv "${wrf_src}/phys/module_sf_noahmp_groundwater.F" "${wrf_src}/phys/module_sf_noahmp_groundwater.F-unpolar"
mv "${wrf_src}/phys/module_sf_noahmpdrv.F" "${wrf_src}/phys/module_sf_noahmpdrv.F-unpolar"
mv "${wrf_src}/phys/module_sf_noahmplsm.F" "${wrf_src}/phys/module_sf_noahmplsm.F-unpolar"
mv "${wrf_src}/phys/module_sf_sfclayrev.F" "${wrf_src}/phys/module_sf_sfclayrev.F-unpolar"

mv "${wrf_src}/phys/module_surface_driver.F" "${wrf_src}/phys/module_surface_driver.F-unpolar"

#not part of the original WRF files
#mv "${wrf_src}/phys/noah.albedo.F" "${wrf_src}/phys/noeh.albedo.F-unpolar"

# registry folder
mv "${wrf_src}/Registry/Registry.EM_COMMON" "${wrf_src}/Registry/Registry.EM_COMMON-unpolar"

# run folder
mv "${wrf_src}/run/GENPARM.TBL" "${wrf_src}/run/GENPARM.TBL-unpolar"
mv "${wrf_src}/run/LANDUSE.TBL" "${wrf_src}/run/LANDUSE.TBL-unpolar"
mv "${wrf_src}/run/MPTABLE.TBL" "${wrf_src}/run/MPTABLE.TBL-unpolar"
mv "${wrf_src}/run/SOILPARM.TBL" "${wrf_src}/run/SOILPARM.TBL-unpolar"
mv "${wrf_src}/run/URBPARM.TBL" "${wrf_src}/run/URBPARM.TBL-unpolar"
mv "${wrf_src}/run/VEGPARM.TBL" "${wrf_src}/run/VEGPARM.TBL-unpolar"

# share folder
mv "${wrf_src}/share/module_soil_pre.F" "${wrf_src}/share/module_soil_pre.F-unpolar"

#####
##### LINK THE FILES
#####

echo "Linking Polar wrf source files"

# check file names and us -sf to force updates to existing links

ln -sf "${pwrf_src}/share/module_soil_pre.F.PWRF4.5.0" "${wrf_src}/share/module_soil_pre.F"

# dyn_em folder
ln -sf "${pwrf_src}/dyn_em/module_first_rk_step_part1.F.PWRF4.5.0" "${wrf_src}/dyn_em/module_first_rk_step_part1.F"
ln -sf "${pwrf_src}/dyn_em/module_initialize_real.F.PWRF4.5.0" "${wrf_src}/dyn_em/module_initialize_real.F"

#phys folder
ln -sf "${pwrf_src}/phys/module_mp_morr_two_moment.F.PWRF4.5.0" "${wrf_src}/phys/module_mp_morr_two_moment.F"
ln -sf "${pwrf_src}/phys/module_mp_p3.F.PWRF4.5.0" "${wrf_src}/phys/module_mp_p3.F"
ln -sf "${pwrf_src}/phys/module_mp_thompson.F.PWRF4.5.0" "${wrf_src}/phys/module_mp_thompson.F"

ln -sf "${pwrf_src}/phys/module_sf_noah_seaice_drv.F.PWRF4.5.0" "${wrf_src}/phys/module_sf_noah_seaice_drv.F"
ln -sf "${pwrf_src}/phys/module_sf_noah_seaice.F.PWRF4.5.0" "${wrf_src}/phys/module_sf_noah_seaice.F"

ln -sf "${pwrf_src}/phys/module_sf_noahdrv.F.PWRF4.5.0" "${wrf_src}/phys/module_sf_noahdrv.F"
ln -sf "${pwrf_src}/phys/module_sf_noahlsm_glacial_only.F.PWRF4.5.0" "${wrf_src}/phys/module_sf_noahlsm_glacial_only.F"
ln -sf "${pwrf_src}/phys/module_sf_noahlsm.F.PWRF4.5.0" "${wrf_src}/phys/module_sf_noahlsm.F"

ln -sf "${pwrf_src}/phys/module_sf_noahmp_glacier.F.PWRF4.5.0" "${wrf_src}/phys/module_sf_noahmp_glacier.F"
ln -sf "${pwrf_src}/phys/module_sf_noahmp_groundwater.F.PWRF4.5.0" "${wrf_src}/phys/module_sf_noahmp_groundwater.F"
ln -sf "${pwrf_src}/phys/module_sf_noahmpdrv.F.PWRF4.5.0" "${wrf_src}/phys/module_sf_noahmpdrv.F"
ln -sf "${pwrf_src}/phys/module_sf_noahmplsm.F.PWRF4.5.0" "${wrf_src}/phys/module_sf_noahmplsm.F"
ln -sf "${pwrf_src}/phys/module_sf_sfclayrev.F.PWRF4.5.0" "${wrf_src}/phys/module_sf_sfclayrev.F"

ln -sf "${pwrf_src}/phys/module_surface_driver.F.PWRF4.5.0" "${wrf_src}/phys/module_surface_driver.F"

#not part of the original WRF files
#mv "${wrf_src}/phys/noah.albedo.F "${wrf_src}/phys/noeh.albedo.F-unpolar

# registry folder
ln -sf "${pwrf_src}/Registry/Registry.EM_COMMON.PWRF4.5.0" "${wrf_src}/Registry/Registry.EM_COMMON"

# run folder
ln -sf "${pwrf_src}/run/GENPARM.TBL.PWRF4.5.0" "${wrf_src}/run/GENPARM.TBL"
ln -sf "${pwrf_src}/run/LANDUSE.TBL.PWRF4.5.0" "${wrf_src}/run/LANDUSE.TBL"
ln -sf "${pwrf_src}/run/MPTABLE.TBL.PWRF4.5.0" "${wrf_src}/run/MPTABLE.TBL"
ln -sf "${pwrf_src}/run/SOILPARM.TBL.PWRF4.5.0" "${wrf_src}/run/SOILPARM.TBL"
ln -sf "${pwrf_src}/run/URBPARM.TBL.PWRF4.5.0" "${wrf_src}/run/URBPARM.TBL"
ln -sf "${pwrf_src}/run/VEGPARM.TBL.PWRF4.5.0" "${wrf_src}/run/VEGPARM.TBL"

# share folder
ln -sf "${pwrf_src}/share/module_soil_pre.F.PWRF4.5.0" "${wrf_src}/share/module_soil_pre.F"

# Copy the WPS files over
echo "Moving into WPS source"

mv "${wps_src}/geogrid/GEOGRID.TBL" "${wps_src}/geogrid/GEOGRID.TBL.ARW.PWRF4.1.1-unpolar"
mv "${wps_src}/metgrid/METGRID.TBL" "${wps_src}/metgrid/METGRID.TBL.ARW.PWRF4.1.1-unpolar"

echo "Linking new tbl files"

ln -sf "${pwrf_src}/wps/geogrid/GEOGRID.TBL.ARW.PWRF4.5.0" "${wps_src}/geogrid/GEOGRID.TBL"
ln -sf "${pwrf_src}/wps/metgrid/METGRID.TBL.ARW.PWRF4.5.0" "${wps_src}/metgrid/METGRID.TBL"

echo "Now recompile WRF and WPS"
```

## Now build WRF serial

For configure choose option **64** and nesting **0**

```bash
./clean -a
./configure
```
Compile WRF. If you would like to capture the output as a log to make sure there were no issues you can do the follwoing
`./compile -j 4 em_real &> wrf_compile_serial.log`

Otherwise, you can compile and install PolarWRF using the following steps. Note - if you see errors during the compile, recompile without the `-j 4` option if you used it, as multiprocessor compiling may cause issues.

```bash
./compile -j 1 em_real
install --target-directory="$WRF_BIN" --mode=0775 main/*.exe
```

## Now build WRF parallel

For configure choose option **66** and nesting **1**

```bash
./clean -a 
./configure
```

**Patch the config file for MPI**

Before compiling, you'll need to update the generated config file to add some additional flags. Copy and paste this into a terminal window, you should see a confirmation that the patch succeeded at both points. Then move on to compiling.

```bash
patch -p1 <<EOT
--- A/configure.wrf 2020-12-10 14:06:01.907649095 -0500
+++ B/configure.wrf 2020-12-10 14:40:00.791338460 -0500
@@ -118,8 +118,8 @@
 SFC             =       ifort
 SCC             =       icc
 CCOMP           =       icc
-DM_FC           =       mpif90 -f90=\$(SFC)
-DM_CC           =       mpicc -cc=\$(SCC)
+DM_FC           =       mpif90
+DM_CC           =       mpicc
 FC              =       time \$(DM_FC)
 CC              =       \$(DM_CC) -DFSEEKO64_OK 
 LD              =       \$(FC)
@@ -140,7 +140,7 @@
 BYTESWAPIO      =       -convert big_endian
 RECORDLENGTH    =       -assume byterecl
 FCBASEOPTS_NO_G =       -ip -fp-model precise -w -ftz -align all -fno-alias \$(FORMAT_FREE) \$(BYTESWAPIO) -xHost -fp-model fast=2 -no-heap-arrays -no-prec-div -no-prec-sqrt -fno-common -xCORE-AVX2
-FCBASEOPTS      =       \$(FCBASEOPTS_NO_G) \$(FCDEBUG)
+FCBASEOPTS      =       \$(FCBASEOPTS_NO_G) \$(FCDEBUG) -assume nocc_omp
 MODULE_SRCH_FLAG =     
 TRADFLAG        =      -traditional-cpp
 CPP             =      /lib/cpp -P -nostdinc
EOT

./compile -j 4 em_real
```

```bash
for exe in main/*.exe; do
  # Install each exe to WRF_BIN with the prefix "mpi_" on it
  # to differentiate from the serial variants:
  WRF_ROOT="$(echo $exe | sed -e 's/main\///')"
  install --mode=0775 "$exe" "${WRF_BIN}/mpi_${WRF_ROOT}"
done
```

For PolarWRF 4.5 - real.exe will fail on compile because of newer compilers and issues with hailcast among others.

Build regular WRF with ./compile em_real

Then, run the script to copy the polar WRF source files

Run clean -a
Run configure
Run compile wrf

This will skip the compilation of real.exe 

Other option is fixing the hailcast line in the Registry - trying that now

Patching the Registry file to fix the hailcast config which will prevent compiler errors on em_real target

```bash
patch -p1 <<EOT
--- A/Registry.EM_COMMON.PWRF4.5.0
+++ B/Registry.EM_COMMON.PWRF4.5.0
@@ -3275,7 +3275,7 @@
 state    real   HAILCAST_DIAM_STD   ij   misc        1         -      -          "HAILCAST_DIAM_STD"   "WRF-HAILCAST Stand. Dev. Hail Diameter" "mm"
 state    real   HAILCAST_WUP_MASK   ij     misc        1         -      r        "HAILCAST_WUP_MASK"           "Updraft mask, 1 if > 10m/s"                             ""
 state    real   HAILCAST_WDUR       ij     misc        1         -      r        "HAILCAST_WDUR"               "Updraft duration"                                       "sec"
-state    real   haildtacttime        -       -         -         -      r        "haildtacttime"              "HAILDTACTTIME"         "HAILCAST ACTIVATION TIME in s"
+state    real   haildtacttime       ij     misc        1         -      r        "haildtacttime"              "HAILDTACTTIME"         "HAILCAST ACTIVATION TIME in s"
 
 
 package   hailcast  hailcast_opt==1        -                    state:hailcast_diam_max,hailcast_diam_mean,hailcast_diam_std,hailcast_dhail1,hailcast_dhail2,hailcast_dhail3,hailcast_dhail4,hailcast_dhail5
EOT
```