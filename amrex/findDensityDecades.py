#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from MakeDataFile import MakeDataFile

def findDensityDecades():

    useEvery = 1

    ID = 'AdiabaticCollapse_XCFC_old'
    idSuffix = '_old'

    plotfileDirectory \
      = '/home/kkadoogan/Work/Codes/thornado/SandBox/AMReX/Applications/' \
        + '{:}/{:}/'.format( ID, ID + idSuffix )

    ID += idSuffix

    plotfileBaseName = ID + '.plt'

    dataDirectory = '.{:}/'.format( ID )

    SSi = -1
    SSf = -1
    nSS = -1

    Field = 'PF_D'
    yLabel = r'$\rho\,\left[\mathrm{g\,cm}^{-3}\right]$'

    plotfileArray \
      = MakeDataFile( Field, plotfileDirectory, dataDirectory, \
                      plotfileBaseName, 'spherical', \
                      SSi = SSi, SSf = SSf, nSS = nSS, \
                      UsePhysicalUnits = True, \
                      MaxLevel = -1, Verbose = True )

    if SSi == -1: SSi = 0
    if SSf == -1: SSf = plotfileArray.shape[0]-1
    if nSS == -1: nSS = plotfileArray.shape[0]

    nSS = nSS // useEvery

    densityDecades = np.logspace( 10, 14, 5 )
    nDecades = densityDecades.shape[0]

    foundDecade = [ False for iDecade in range( nDecades ) ]
    foundDecade = np.array( foundDecade, bool )

    ind = np.empty( (nDecades), np.int64   )
    t   = np.empty( (nDecades), np.float64 )

    SS = np.linspace( SSi, SSf, nSS, dtype = np.int64 )

    density    = 0.0
    MaxDensity = 0.0
    tMax       = 0.0
    indMax     = 0

    fig, ax = plt.subplots( 1, 1 )

    for iSS in range( nSS ):

        if iSS % useEvery == 0:
          print( '  {:}/{:}'.format( iSS, nSS ) )

        fileDirectory = dataDirectory + plotfileArray[SS[iSS]] + '/'

        timeFile = fileDirectory + '{:}.dat'.format( 'Time' )
        dataFile = fileDirectory + '{:}.dat'.format( Field  )

        data = np.loadtxt( dataFile )
        time = np.loadtxt( timeFile )

        density = data[0]

        if density > MaxDensity:

            MaxDensity = density
            tMax       = time
            indMax     = SS[iSS]

        for iDecade in range( nDecades ):

            if density > densityDecades[iDecade] and not foundDecade[iDecade]:

                X1File = fileDirectory + '{:}.dat'.format( 'X1'   )
                X1_C   = np.loadtxt( X1File   )

                foundDecade[iDecade] = True
                ind        [iDecade] = SS[iSS]
                t          [iDecade] = time

                ax.plot( X1_C, data )

    ax.grid( which = 'both' )

    ax.set_xscale( 'log' )
    ax.set_yscale( 'log' )

    ax.set_xlabel( r'$r\,\left[\mathrm{km}\right]$' )
    ax.set_ylabel( yLabel )

    plt.show()
    plt.close()

    print( ind )
    print( 'MaxDensity: {:.3e} g/cm^3'.format( MaxDensity ) )
    print( '      tMax: {:.3e} ms'.format( tMax ) )
    print( '    indMax: {:d}'.format( indMax ) )

if __name__ == '__main__':

    findDensityDecades()

    import os
    os.system( 'rm -rf __pycache__' )
