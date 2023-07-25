#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

from UtilitiesModule import GetFileArray
from MakeDataFile import MakeDataFile, ReadHeader

def findDensityDecades():

    ID = 'AdiabaticCollapse_XCFC'

    plotfileDirectory \
      = '/Users/dunhamsj/Work/Codes/thornado/SandBox/AMReX/Applications/' \
        + '{:}/{:}_000-479.2ms/'.format( ID, ID )

    plotfileBaseName = ID + '.plt'

    datafileDirectory = '.{:}/'.format( ID )

    plotfileArray = GetFileArray( plotfileDirectory, plotfileBaseName )

    for iSS in range( plotfileArray.shape[0] ):
        plotfileArray[iSS] = plotfileArray[iSS][-8:]

    SSi = 0
    SSf = plotfileArray.shape[0] - 1
    nSS = plotfileArray.shape[0]

    MakeDataFile( 'PF_D', plotfileDirectory, datafileDirectory, \
                  plotfileBaseName, 'spherical', \
                  SSi = SSi, SSf = SSf, nSS = nSS, \
                  UsePhysicalUnits = True, \
                  MaxLevel = -1, Verbose = True )

    densityDecades = np.logspace( 10, 14, 5 )
    nDecades = densityDecades.shape[0]

    foundDecade = [ False for iDec in range( nDecades ) ]
    foundDecade = np.array( foundDecade, bool )

    ind = np.empty( (nDecades), np.int64   )
    t   = np.empty( (nDecades), np.float64 )

    density    = 0.0
    MaxDensity = 0.0
    tMax       = 0.0
    indMax     = 0

    i = 0
    for iSS in range( nSS ):

        i += 1

        iSS = SSi + np.int64( ( SSf - SSi  ) / ( nSS - 1 ) * iSS )

        if i % 100 == 0:
          print( '  {:}/{:}'.format( i, nSS ) )

        timefile = datafileDirectory + plotfileArray[iSS] + '/Time.dat'
        datafile = datafileDirectory + plotfileArray[iSS] + '/PF_D.dat'

        dataShape, dataUnits, minVal, maxVal \
          = ReadHeader( datafile )

        data = np.loadtxt( datafile ).reshape( np.int64( dataShape ) )
        time = np.loadtxt( timefile )
        density = data[0]

        if density > MaxDensity:

            MaxDensity = density
            tMax       = time
            indMax     = iSS

        for iDec in range( nDecades ):

            if density > densityDecades[iDec] and not foundDecade[iDec]:

                foundDecade[iDec] = True
                ind        [iDec] = iSS
                t          [iDec] = time

    print( ind )
    print( 'MaxDensity: {:.3e} g/cm^3'.format( MaxDensity ) )
    print( '      tMax: {:.3e} ms'.format( tMax ) )
    print( '    indMax: {:d}'.format( indMax ) )

    MaxDensity = MaxDensity
    tMax       = tMax
    indMax     = indMax

#if __name__ == '__main__':

findDensityDecades()

import os
os.system( 'rm -rf __pycache__' )
