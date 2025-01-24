# MPAS Install on Caviness

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

## Bulding the IO Libraries

MPAS requires NetCDF, Parallel-NetCDF, and ParallelIO (PIO). Tested versions of the libraries are:
- NetCDF 4.4.x
- Parallel-NetCDF 1.8.x
- PIO 2.x or 1.9.23

[PIO Website](https://ncar.github.io/ParallelIO/)

PIO Download
`git clone https://github.com/NCAR/ParallelIO.git`



