#!/bin/bash

# Sets the directories and flags for WRF 4.5

vpkg_require openmpi/4.0.2:intel

WRF_PREFIX=/work/regc/ryWRF/wrf455

WRF_SRC="${WRF_PREFIX}/src"
WRF_BIN="${WRF_PREFIX}/bin"
WRF_INC="${WRF_PREFIX}/include"
WRF_LIB="${WRF_PREFIX}/lib"
WRF_LIBRARIES_SRC="${WRF_SRC}/LIBRARIES"
WRF_TESTS_SRC="${WRF_SRC}/TESTS"

export CC=icc
export CFLAGS="-xHost"
export CXX=icpc
export CXXFLAGS="-xHost"
export CPPFLAGS="-I${WRF_INC}"
export FC=ifort
export FCFLAGS="-I${WRF_INC} -xHost" 
export F77="$FC"
export LDFLAGS="-L${WRF_LIB}"
export PATH="${WRF_BIN}:$PATH"
export MPICC="mpicc"
export MPICXX="mpicxx"
export MPIFC="mpifort"

export LD_LIBRARY_PATH="/work/regc/ryWRF/wrf455/lib:${LD_LIBRARY_PATH}"
export PATH="/work/regc/ryWRF/wrf455/bin:/work/regc/ryWRF/wrf455/lib:${PATH}"
export JASPERLIB="/work/regc/ryWRF/wrf455/lib"
export JASPERINC="/work/regc/ryWRF/wrf455/include"
export NETCDF="/work/regc/ryWRF/wrf455"
