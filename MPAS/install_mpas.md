# MPAS Install on Caviness

# Table of Contents
1. [Preliminaries](#preliminaries)
2. [Setting Up Your Environment](#setting-up-your-environment)
 

This document will walk you through downloading and compiling NCAR/UCAR MPAS (Model for Prediction Across Scales) on UD's Caviness cluster.

MPAS Documentation is available from the [MPAS Homepage](https://mpas-dev.github.io)
MPAS User Manual as a PDF can be downloaded from this link [MPAS 8.2.0 User Manual](https://www2.mmm.ucar.edu/projects/mpas/mpas_atmosphere_users_guide_8.2.0.pdf)
MPAS Online Tutorial is available here [MPAS Tutorial](https://www2.mmm.ucar.edu/projects/mpas/tutorial/v8.0/index.html)

## Preliminaries

There are a few things you'll want to make sure of before you get started, that is, making sure you set your working group.

`workgroup -g regc`

**Note that whenever you set your workgroup it creates a new shell so you will need to source any environment seutp scripts again.**

### Setting Up Your Environment

The following section covers adding environment variables required for building and running MPAS and related libraries, along with loading the necessary valet packages on Caviness.

MPAS requires C and Fortran compilers, specifically a fortran compiler that will support the ISO_C_BINDING module from the Fortran 2003 standard and procedure pointer components of derived types. On Caviness we'll use the Intel compiler suite which will meet this requirement. 

You will need make sure you always load the OpenMPI valet package either during the building of MPAS and then whenever you run MPAS. We'll add this to the environment setup script we create below.

To run the OpenMPI valet package:
`vpkg_require openmpi/4.0.2:intel`

Next we want to set some directories for our libraries to install into and for the compilers to find the necessary include and library files. In your working directory create a folder for all of your libraries, I called mine rySharedLibraries. In that folder, create the following folders structure: 

rySharedLibraries    
 |  
 +--bin  
 |  
 +--lib  
 |  
 +--include  
 |   
 +--src  
 |  
 +--share  

As we build each library, the corresponding files will be installed into the above folders. We'll add these to the proper environment variables so the compilers can find these libraries when building MPAS.

This will create the environment variables for the library directories and add them to our PATH and LD_LIBRARY_PATH.

```bash
export LIBBASE=/work/regc/rySharedLibraries
export LIBSRC=/work/regc/rySharedLibraries/src
export PATH=${LIBBASE}/bin:${LIBBASE}/lib:$PATH
export LD_LIBRARY_PATH=${LIBBASE}/lib:$LD_LIBRARY_PATH
```

The next set of environment variables will set which compilers and compiler flags we'll be using. On Caviness we'll be using the Intel compilers and also adding flags for these compilers to point to our new libraries folders.

```bash
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
```

MPAS requires NetCDF, Parallel-NetCDF, and ParallelIO (PIO). Tested versions of the libraries are:
- ZLib 1.2.11
- HDF5 1.10.5
- NetCDF-C 4.4.x
- NetFortran 4.4.x
- Parallel-NetCDF 1.8.x
- PIO 2.x or 1.9.23

Most of the above library files can be downloaded from Michael Duda's [website](https://www2.mmm.ucar.edu/people/duda/files/mpas/sources/) at NCAR. Michael Duda is one of the key software developers for WPS/WRF/MPAS.

On Caviness, the compressed files can be copied from this directory:
`/work/regc/rySharedLibraries/source/archive_files`

To copy the files if you are on Caviness, you can use the following command:
`cp /work/regc/rySharedLibraries/src/archive_files/* $LIBBASE/src/`
This will copy all of the files into your src folder within your library folder.

To download the necessary compressed files from Duda's website, follow these steps:

```bash
cd $LIBBASE/src
wget https://www2.mmm.ucar.edu/people/duda/files/mpas/sources/zlib-1.2.11.tar.gz
wget https://www2.mmm.ucar.edu/people/duda/files/mpas/sources/hdf5-1.10.5.tar.bz2
wget https://github.com/Unidata/netcdf-c/archive/v4.7.2.tar.gz
wget https://github.com/Unidata/netcdf-fortran/archive/v4.5.2.tar.gz
wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/libpng-1.2.50.tar.gz
wget https://parallel-netcdf.github.io/Release/pnetcdf-1.12.2.tar.gz
```

Once you've downloaded or copied the library files to your src folder, you can expand the archive files.
`tar -xf filename.tar.gz` 

Parallel IO will need to be downloaded from Github:

[PIO Website](https://ncar.github.io/ParallelIO/)

PIO Download
`git clone https://github.com/NCAR/ParallelIO.git`

Add instructions and links to go to the release pages for each of these libraries on GitHub to download.



### ZLib Build

```bash
cd $LIBBASE/src/zlib-1.2.11/
./configure --prefix=${LIBBASE}
make
make install
cd ..
```

### HDF5 Build

```bash
cd $LIBBASE/src/hdf5-1.10.5/
export FC=$MPIFC
export CC=$MPICC
export CXX=$MPICXX
./configure --prefix=${LIBBASE} --enable-parallel --with-zlib=${LIBBASE} --enable-fortran --disable-shared
make
make install

# now undo the exports
export FC=ifort
export CC=icc
export CXX=icpc
```

### Parallel-netCDF

```console
cd $LIBBASE/src/pnetcdf-1.12.2/
./configure --prefix=${LIBBASE} --disable-shared
make
make install
```


### netCDF-C

```console
cd $LIBBASE/src/netcdf-c-4.7.2
export CPPFLAGS="-I${LIBBASE}/include"
export LDFLAGS="-L${LIBBASE}/lib"
export LIBS="-lhdf5_hl -lhdf5 -lz -ldl"
export CC=$MPICC
./configure --prefix=${LIBBASE} --disable-dap --enable-netcdf4 --enable-pnetcdf --enable-cdf5 --disable-shared
make
make install

# undo the exports
```


### netCDF-Fortran

Make sure the CC variable is still set to $MPICC, otherwise the linking of the NetCDF C libraries will not work.

```console
export FC=$MPIFC
export F77=$MPIF77
export LIBS="-lnetcdf -lpnetcdf ${LIBS}"
LDFLAGS="$(nc-config --libs --static)" ./configure --prefix=${LIBBASE} --disable-shared
make
make install

#undo export
export FC=ifort
export F77=ifort
export CC=icc
```

### PIO


```console
LDFLAGS="(nc-config --libs --static)" ./configure --prefix=${LIBBASE} --enable-fortran --disable-shared
make
make install
```


notes from forum
make pgi CORE=atmosphere PRECISION=single PIO=/usr/local USE_PIO2=true 'LDFLAGS_OPT=-O3
