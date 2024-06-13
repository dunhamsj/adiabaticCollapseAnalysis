#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from MakeDataFile import MakeDataFile

def findShockRadii():

    useEvery = 1

    # These numbers come from running findDensityDecades.py
    tb        = 2.530e2
    indBounce = 253

    ID = 'AdiabaticCollapse_XCFC_newCP'
    idSuffix = ''

    #plotfileDirectory \
    #  = '/home/kkadoogan/Work/Codes/thornado/SandBox/AMReX/Applications/' \
    #    + '{:}/{:}/'.format( ID, ID + idSuffix )
    plotfileDirectory \
      = '/home/kkadoogan/' \
        + '{:}/'.format( ID, ID + idSuffix )

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

    rSh = np.zeros( (nSS), np.float64 )
    tSh = np.zeros( (nSS), np.float64 )

    SS = np.linspace( SSi, SSf, nSS, dtype = np.int64 )

    for iSS in range( SS.shape[0] ):

        if iSS % useEvery == 0:
            print( '  {:}/{:}'.format( iSS, nSS ) )

        if SS[iSS] < indBounce: continue

        fileDirectory = dataDirectory + plotfileArray[SS[iSS]] + '/'

        timeFile = fileDirectory + '{:}.dat'.format( 'Time' )
        X1File   = fileDirectory + '{:}.dat'.format( 'X1'   )
        dataFile = fileDirectory + '{:}.dat'.format( Field  )

        time = np.loadtxt( timeFile )
        X1_C = np.loadtxt( X1File   )
        data = np.loadtxt( dataFile )

        indCO = np.where( X1_C > 15.0 )[0]
        data  = np.copy( np.log10( data[indCO] ) )
        X1_C  = np.copy( X1_C[indCO] )

        diff = np.abs( np.diff( data ) ) / data[:-1]

        indRs    = np.argmax( diff )
        xS       = X1_C[indRs]
        gradient = diff[indRs]

        tSh[iSS] = time
        rSh[iSS] = xS

    shockRadii = np.array( [ 1.0e2, 5.0e2, 1.0e3, 2.0e3, 4.0e3 ] )
    nRadii = shockRadii.shape[0]

    foundRadius = [ False for iRadius in range( nRadii ) ]
    foundRadius = np.array( foundRadius )

    time = np.zeros( (nRadii), np.float64 )
    ind  = np.zeros( (nRadii), np.int64   )

    fig, ax = plt.subplots( 1, 1 )

    ax.set_title( r'$\texttt{{{:}}}$'.format( ID ) )

    plotfileDirectory \
      = '/home/kkadoogan/' \
        + '{:}/'.format( ID, ID + idSuffix )

    for iSS in range( SS.shape[0] ):

        if SS[iSS] < indBounce: continue

        for iRadius in range( nRadii ):

            if rSh[iSS] > shockRadii[iRadius] \
                 and not foundRadius[iRadius]:

                foundRadius[iRadius] = True
                ind        [iRadius] = SS [iSS]
                time       [iRadius] = tSh[iSS]

                fileDirectory = dataDirectory + plotfileArray[SS[iSS]] + '/'

                timeFile = fileDirectory + '{:}.dat'.format( 'Time' )
                X1File   = fileDirectory + '{:}.dat'.format( 'X1'   )
                dataFile = fileDirectory + '{:}.dat'.format( Field  )

                t = np.loadtxt( timeFile )
                X1_C = np.loadtxt( X1File   )
                data = np.loadtxt( dataFile )

                ax.plot( X1_C, data, \
                         label = r'$t-t_b={:d}\, \mathrm{{ms}}$' \
                                 .format( np.int64( t - tb ) ) )

    for i in range( nRadii ):
        ax.axvline( shockRadii[i], color = 'k' )

    ax.grid( which = 'both' )

    ax.set_xscale( 'log' )
    ax.set_yscale( 'log' )

    ax.set_xlabel( r'$r\,\left[\mathrm{km}\right]$' )
    ax.set_ylabel( yLabel )

    ax.legend()

    plt.show()

    print( 'time =', time )
    print( 'ind  =', ind  )

if __name__ == '__main__':

    findShockRadii()

    import os
    os.system( 'rm -rf __pycache__' )
