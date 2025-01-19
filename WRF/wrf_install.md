# WRF Installation on Caviness

This document will walk you through compiling WRF on the Caviness cluster.

## Login and Workgroup

Once you've logged into Caviness, the first step is to set your workgroup. Remember to do this everytime you log in.

`workgroup -g regc`

## Set Your Environment Variables

The following commands will set environment variables that WRF and the related libraries will use to find their installation locations and compiler configurations. These are only set for the current session. If you exit your workgrouop and/or logout of Caviness before you complete the install, you'll need to set these again.

If you set them before changing your workgroup, which starts a new shell session, you'll have to set them again, so be sure to change your workgorup immediately after logging in.

## Caviness OpenMPI

You'll need to make sure you activate the OpenMPI package on Caviness before you begin, otherwise you will not be able to compile and/or run WRF.

```bash
vpkg_require openmpi/4.0.2:intel
```

You may also want to add this to your bash.rc or bash.profile scripts so it is always loaded.

### Environment Variables

Copy paste each line into the terminal and press enter to execute it. Be sure to change the first line to match where you want to setup your WRF and make sure the directory has been created.

```bash
WRF_PREFIX=$WORKDIR/polarWRF/pWRF_4_5_1
mkdir -p "$WRF_PREFIX"

WRF_SRC="${WORKDIR}/polarWRF/WRF"
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
```

## Support Libraries Installation

First, create the directories:

```bash
mkdir $WRF_PREFIX
mkdir $WRF_SRC
mkdir $WRF_LIBRARIES_SRC
```

Download the required libraries into the WRF source directory.

```bash
cd "$WRF_LIBRARIES_SRC"
wget https://www2.mmm.ucar.edu/people/duda/files/mpas/sources/zlib-1.2.11.tar.gz
wget https://github.com/Unidata/netcdf-c/archive/v4.7.2.tar.gz
wget https://github.com/Unidata/netcdf-fortran/archive/v4.5.2.tar.gz
wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/libpng-1.2.50.tar.gz
wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/jasper-1.900.1.tar.gz
```

### Build and Install Each Library

The following steps will walk you through compiling each library, the installing the related library files into the $WRF_PREFIX folder so WRF can find them when it is compiled.

It is important to follow the ./configure flags for the libraries to be compiled properly. disable-shared is key as the cluster has multiple instances of libraries and this will cause issues for the compiler.

### ZLIB

Install the ZLib Library.

```bash
tar xzvf zlib-1.2.11.tar.gz
cd zlib-1.2.11
./configure --prefix=$WRF_PREFIX
make
make install
cd ..
```

### NetCDF-c

Install the NetCDF-c library.

```bash

tar -xf v4.7.2.tar.gz
cd netcdf-c-4.7.2
./configure --disable-shared --disable-netcdf4 --disable-dap --prefix=$WRF_PREFIX
make -j 4
make check
make install
cd ..
```

### NetCDF-fortran

Install the NetCDF-fortran library.

```bash
tar -xf v4.5.2.tar.gz
cd netcdf-fortran-4.5.2
./configure --disable-shared --prefix=$WRF_PREFIX
make -j 4
make install
cd ..
```

### libpng

Install the libpng library.

```bash

tar xzvf libpng-1.2.50.tar.gz
cd libpng-1.2.50
./configure --prefix=$WRF_PREFIX
make -j 4
make install
cd ..
```

### jasper

Install the jasper library.

```bash

tar xzvf jasper-1.900.1.tar.gz
cd jasper-1.900.1
./configure --prefix=$WRF_PREFIX
make -j 4
make install
cd ..
```

# TESTS

The following tests ensure that the netcdf libraries are compiled and configured correctly.

Download and tar the test files:

```bash
mkdir "$WRF_TESTS_SRC"
cd "$WRF_TESTS_SRC"

wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/Fortran_C_NETCDF_MPI_tests.tar
tar -xf Fortran_C_NETCDF_MPI_tests.tar
```

Compile, link and test the single processor configuration:

```bash
$FC $FCFLAGS -c 01_fortran+c+netcdf_f.f $LDFLAGS
$CC $CPPFLAGS -c 01_fortran+c+netcdf_c.c $CFLAGS $LDFLAGS
$FC -c 01_fortran+c+netcdf_f.f $FCFLAGS $LDFLAGS
$CC $CPPFLAGS -c 01_fortran+c+netcdf_c.c $CFLAGS $LDFLAGS
$FC 01_fortran+c+netcdf_f.o 01_fortran+c+netcdf_c.o $FCFLAGS $LDFLAGS -lnetcdff -lnetcdf
./a.out
```

Your results should look like this:

```bash
[(regc:reagan)@login01.caviness TESTS]$ ./a.out
   C function called by Fortran
   Values are xx =  2.00 and ii = 1 
 SUCCESS test 1 fortran + c + netcdf
 ```

Compile, link and test the multiple processor configuration:

```bash
$MPICC $CPPFLAGS -c 02_fortran+c+netcdf+mpi_c.c $CFLAGS $LDFLAGS
$MPIFC -c 02_fortran+c+netcdf+mpi_f.f $FCFLAGS $LDFLAGS
$MPICC $CPPFLAGS -c 02_fortran+c+netcdf+mpi_c.c $CFLAGS $LDFLAGS
$MPIFC 02_fortran+c+netcdf+mpi_f.o 02_fortran+c+netcdf+mpi_c.o $FCFLAGS $LDFLAGS -lnetcdff -lnetcdf
mpirun -np 2 ./a.out
```

Your results should look like this:

```bash
[(regc:reagan)@login01.caviness TESTS]$ mpirun -np 2 ./a.out
   C function called by Fortran
   Values are xx =  2.00 and ii = 1 
   C function called by Fortran
   Values are xx =  2.00 and ii = 1 
 status =            2
 status =            2
 SUCCESS test 2 fortran + c + netcdf + mpi
 SUCCESS test 2 fortran + c + netcdf + mpi
```

# Install WRF

```bash
cd $WRF_SRC
git clone --recurse-submodules https://github.com/wrf-model/WRF
cd WRF
git tag -l ##lists the releases
git checkout tags/v#.#.#
```

## Now build WRF serial

Note - if you see errors during the compile, recompile without the `-j 4` option, as multiprocessor compiling may cause issues.

For configure choose option **64** and nesting **0**

```bash
./configure
./compile -j 4 em_real
makedir -p "$WRF_BIN"
install --target-directory="$WRF_BIN" --mode=0775 main/*.exe
```

## Now build WRF parallel

For configure choose option **66** and nesting **1**

```bash
./clean -a 
./configure
```

**Patch the config file for MPI**

◊

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

# Install WPS

## Get WPS code

```bash
git clone https://github.com/wrf-model/WPS
git tag -l ##lists the releases
git checkout tags/v#.#.#
```

### Build WPS Serial

Choose option **17**

```bash
./configure
./compile
install --target-directory="$WRF_BIN" --mode=0775 *.exe
```

### Build WPS parallel

Choose option **19**

```bash
./clean -a
./configure
./compile
for exe in *.exe; do
**Install each exe to WRF_BIN with the prefix "mpi_" on it**
**to differentiate from the serial variants:**
  install --mode=0775 "$exe" "${WRF_BIN}/mpi_${exe}"
done
```

**Great! You should have successfully installed WRF**

