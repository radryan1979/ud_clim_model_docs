#!/bin/bash

# Sets the directories and flags for MPAS

vpkg_require openmpi/4.0.2:intel

export LIBBASE=/work/regc/rySharedLibraries
export LIBSRC=/work/regc/rySharedLibraries/src
export LIBRARY_PATH=${LIBBASE}/lib:$LIBRARY_PATH
export PATH=${LIBBASE}/bin:$PATH

export CC=icc
export CFLAGS="-xHost"
export CXX=icpc
export CXXFLAGS="-xHost"
export CPPFLAGS="-I${LIBBASE}/inc"
export FC=ifort
export FCFLAGS="-I${LIBBASE}/inc -xHost" 
export F77="$FC"
export LDFLAGS="-L${LIBBASE}/lib"
export MPICC="mpicc"
export MPICXX="mpicxx"
export MPIFC="mpifort"
export MPIF77="mpifort"
export MPIF90="mpifort"

export PNETCDF=$LIBBASE
export NETCDF=$LIBBASE
export PIO=$LIBBASE

export MPAS_EXTERNAL_LIBS="-L${LIBBASE}/lib -lnetcdf -lpnetcdf -lhdf5_hl -lhdf5 -ldl -lz"
export MPAS_EXTERNAL_INCLUDES="I${LIBBASE}/include"
