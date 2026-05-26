# WRF Installation on Local Ubuntu

WRF will run rather efficiently on a decent desktop workstation or gaming laptop. The big difference is that you'll compile the shared memory parallel code. Details below, but this will allow use of multiple cores to speed up the WRF and REAL programs.

## Basic Requirements

Before you can begin, you'll need to have some basic packages installed. We'll be building WRF with the GNU compiler collection:
- gcc
- g++
- gfortran
- m4
- tsch
- build-essential

First install the build-essential packages that will include the GNU compilers, Make, and some dev libraries. Do not go higher than version 13.4, otherwise nothing will compile properly because of C standard changes.

```bash
sudo apt update
sudo apt upgrade
sudo apt install gcc-13 g++-13 gfortran-13
```

Now check that your compilers have been installed.
```bash
which gfortran
which gcc
gfortran --version
gcc --version
```

You should get a path listing for the first two to something like /usr/bin/gfortran and /usr/bin/gcc

Make sure Perl is installed (it should be)
```bash
perl -v
```
This should give you some information about the version of perl installed. If nothing is returned, install Perl

```bash
sudo apt update
sudo apt install perl
```

Make sure the m4 Macro Processor is installed

```bash
sudo apt install m4
```

Make sure Tcl installed
=======
Make sure tsch installed. You may have to add the universe repository first if you get an unable to locate package message.
```bash
sudo add-apt-repository universe
```
Follow the default prompts. Then run the line below.

```bash
sudo apt install tcl
```

For parallel processing, you'll need to make sure the OpenMP libraries are installed:

```bash
sudo apt install libomp-dev
```

## Setting Up Your Environment 

The following commands will set environment variables that WRF and the related libraries will use to find their installation locations and compiler configurations. These are only set for the current session. If you exit your workgrouop and/or logout of Caviness before you complete the install, you'll need to set these again.

If you set them before changing your workgroup, which starts a new shell session, you'll have to set them again, so be sure to change your workgorup immediately after logging in.


### Environment Variables

Copy paste each line into the terminal and press enter to execute it. Be sure to change the first line to match where you want to setup your WRF and make sure the directory has been created.

```bash
# Sets the directories and flags for WRF 4.5

WRF_PREFIX=/home/ryan/cirrus/Modeling/WRF/WRF455
WRF_DIR=/home/ryan/cirrus/Modeling/WRF/WRF455
WRF_SRC="${WRF_PREFIX}/src"
WRF_BIN="${WRF_PREFIX}/bin"
WRF_INC="${WRF_PREFIX}/include"
WRF_LIB="${WRF_PREFIX}/lib"
WRF_LIBRARIES_SRC="${WRF_SRC}/LIBRARIES"
WRF_TESTS_SRC="${WRF_SRC}/TESTS"

# This tells OpenMP how many cores/threads it can use.
export OMP_NUM_THREADS=8

# Note the flags to prevent new compilers from yelling about poor coding standards
export CC=gcc
export CXX=g++
export CFLAGS=""
export CPPFLAGS="-I${WRF_INC}"
export FC=gfortran
export FCFLAGS="-I${WRF_INC}" 
export F77="$FC"
export LDFLAGS="-L${WRF_LIB}"
export PATH="${WRF_BIN}:$PATH"
export MPICC=gcc
export MPICXX=g++
export MPIFC=gfortran

export LD_LIBRARY_PATH="${WRF_LIB}:${LD_LIBRARY_PATH}"
export PATH="${WRF_BIN}:${WRF_LIB}:${PATH}"
export JASPERLIB="${WRF_LIB}"
export JASPERINC="${WRF_INC}"
export NETCDF="${WRF_PREFIX}"

```
You can make a shell script with the above lines and save it, as you'll need it to setup your environment everytime you run WRF also.

Save the above as a script called `wrf455_env.sh` and then update the permissions to make it executable:
`chmod +x wrf455_env.sh`

Then, once you open a new terminal, you can source this script and it will set all of the environment variables:
`source wrf455_env.sh`

Be sure to source this before continuing on the steps below.

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

You can obtain the WRF source code from the GitHub repository. The best option is to obtain a tar file from the releaes page:
[WRF Releases](https://github.com/wrf-model/WRF/releases)

You can use `wget` to download a give release following the URL below for the version you'd like.

```bash
cd $WRF_SRC
mkdir WRF
cd WRF
wget https://github.com/wrf-model/WRF/releases/download/v4.5.2/v4.5.2.tar.gz
```

The other approach is to checkout the repository, and tag the branch you want. This option is for more advanced users and is not recommended for a stable production build.

```bash
cd $WRF_SRC
git clone --recurse-submodules https://github.com/wrf-model/WRF
cd WRF
git tag -l ##lists the releases
git checkout tags/v#.#.#
```

## Now build WRF serial

Note - if you see errors during the compile, recompile without the `-j 4` option, as multiprocessor compiling may cause issues.

For configure choose option **32** and nesting **0**

```bash
./configure
./compile -j 4 em_real
mkdir -p "$WRF_BIN"
install --target-directory="$WRF_BIN" --mode=0775 main/*.exe
```

## Now build WRF parallel (OpenMP)

For configure choose option **32** and nesting **1**

```bash
./clean -a 
./configure
./compile -j 4 em_real
```

```bash
for exe in main/*.exe; do
  # Install each exe to WRF_BIN with the prefix "mpi_" on it
  # to differentiate from the serial variants:
  WRF_ROOT="$(echo $exe | sed -e 's/main\///')"
  install --mode=0775 "$exe" "${WRF_BIN}/omp_${WRF_ROOT}"
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
#Install each exe to WRF_BIN with the prefix "mpi_" on it
#to differentiate from the serial variants:
  install --mode=0775 "$exe" "${WRF_BIN}/mpi_${exe}"
done
```

**Great! You should have successfully installed WRF**

