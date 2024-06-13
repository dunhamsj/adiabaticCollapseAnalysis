#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
plt.style.use( 'publication.sty' )

from MakeDataFile import MakeDataFile, ReadHeader

"""

Creates a directory with structure as laid out
in MakeDataFile.py and makes a movie from it

Usage:
  $ python3 makeMovie1D.py

"""

#### ========== User Input ==========

tb = 2.503e2

# ID to be used for naming purposes
ID = [ 'AdiabaticCollapse_XCFC_oldCP', 'AdiabaticCollapse_XCFC_newCP' ]
nRuns = len( ID )
lab = [ 'oldCP', 'newCP' ]

HOME = '/home/kkadoogan/'

# Directory containing AMReX plotfiles
plotfileDirectory = [ '/home/kkadoogan/{:}/'.format( IDD ) for IDD in ID ]

# plotfile base name (e.g., Advection1D.plt######## -> Advection1D.plt )
plotfileBaseName = [ IDD + '.plt' for IDD in ID ]

# Field to plot
field = 'AF_E'
yLabel = r'$\epsilon\ \left[\mathrm{erg\,g}^{-1}\right]$'

# Plot data in log10-scale?
useLogScale_Y = True

# Only use every <plotEvery> plotfile
plotEvery = 1

# First and last snapshots and number of snapshots to include in movie
SSi = -1 # -1 -> SSi = 0
SSf = -1 # -1 -> plotfileArray.shape[0] - 1
nSS = -1 # -1 -> plotfileArray.shape[0]

# Max level of refinement to include
maxLevel = -1

verbose = True

useCustomLimits = False
ymin = 1.0e5
ymax = 1.0e15

useCustomTicks_Y = False
yticks = np.logspace( 5, 15, 11 )

movRunTime = 10.0 # seconds

#### ====== End of User Input =======

dataDirectory = [ '.{:}/'.format( IDD ) for IDD in ID ]

fcD = False
owD = False
fcF = False
owF = False

plotfileArray \
  = [ MakeDataFile( field, plotfileDirectory[i], dataDirectory[i], \
                  plotfileBaseName[i], 'spherical', \
                  SSi = SSi, SSf = SSf, nSS = nSS, \
                  UsePhysicalUnits = True, \
                  MaxLevel = maxLevel, \
                  forceChoiceD = fcD, owD = owD, \
                  forceChoiceF = fcF, owF = owF, \
                  Verbose = verbose )[::plotEvery] for i in range( nRuns ) ]

def f(t):

    fileDirectory \
      = [ dataDirectory[i] + plotfileArray[i][t] + '/' \
          for i in range( nRuns ) ]

    timeFile = [ fileDirectory[i] + '{:}.dat'.format( 'Time' ) \
                 for i in range( nRuns ) ]
    X1File   = [ fileDirectory[i] + '{:}.dat'.format( 'X1'   ) \
                 for i in range( nRuns ) ]
    dX1File  = [ fileDirectory[i] + '{:}.dat'.format( 'dX1'  ) \
                 for i in range( nRuns ) ]
    dataFile = [ fileDirectory[i] + '{:}.dat'.format( field  ) \
                 for i in range( nRuns ) ]

    time = [ np.loadtxt( timeFile[i] ) for i in range( nRuns ) ]
    X1_C = [ np.loadtxt( X1File  [i] ) for i in range( nRuns ) ]
    dX1  = [ np.loadtxt( dX1File [i] ) for i in range( nRuns ) ]
    data = [ np.loadtxt( dataFile[i] ) for i in range( nRuns ) ]

    return data, X1_C, dX1, time

data0, X1_C0, dX10, time = f(0)

xL = X1_C0[0][0 ] - 0.5 * dX10[0][0 ]
xH = X1_C0[0][-1] + 0.5 * dX10[0][-1]

if nSS < 0: nSS = min( len( plotfileArray[0] ), len( plotfileArray[1] ) )

fig, ax = plt.subplots( 1, 1 )
ax.set_title( r'$\texttt{AdiabaticCollapse_XCFC}$', fontsize = 15 )

if not useCustomLimits:
    ymin = +np.inf
    ymax = -np.inf
    for j in range( nSS ):
        for i in range( nRuns ):
            dataFile \
              = dataDirectory[i] + plotfileArray[i][j] \
                  + '/{:}.dat'.format( field )
            dataShape, dataUnits, minVal, maxVal = ReadHeader( dataFile )
            ymin = min( ymin, minVal )
            ymax = max( ymax, maxVal )

time_text = ax.text( 0.1, 0.9, '', transform = ax.transAxes, fontsize = 13 )

ax.set_xlabel( r'$r\ \left[\mathrm{km}\right]$', fontsize = 15 )
ax.set_ylabel( yLabel )

ax.set_xlim( xL + 0.25 * dX10[0][0], 1.0e4 )
ax.set_ylim( ymin, ymax )

ax.grid( which = 'both' )

if useLogScale_Y: ax.set_yscale( 'log' )
ax.set_xscale( 'log' )

line = np.empty( nRuns, object )
for i in range( nRuns ):
    line[i], = ax.plot( [],[], '-', label = lab[i] )

ax.legend( loc = 1 )

def InitializeFrame():

    ret = []
    for i in range( nRuns ):
        line[i].set_data([],[])
        ret.append( line[i] )

    time_text.set_text('')
    ret.append( time_text )

    ret = tuple( ret )

    return ret

def UpdateFrame( t ):

    print('    {:}/{:}'.format( t, nSS ) )
    data, X1_C, dX1, time = f(t)

    time = sum( time ) / np.float64( nRuns )

    time_text.set_text( r'$t-t_{{b}}={:.3e}\ \left[\mathrm{{ms}}\right]$' \
                        .format( time - tb ) )

    ret = []
    for i in range( nRuns ):
        line[i].set_data( X1_C[i], data[i].flatten() )
        ret.append( line[i] )

    ret.append( time_text )
    ret = tuple( ret )

    return ret

xRef = [ 4.0e3, 2.0e3, 1.0e3, 5.0e2, 1.0e2, 5.0e1 ]
for xx in xRef:
    ax.axvline( xx, color = 'b', alpha = 0.3 )

if useCustomTicks_Y:
    ax.set_yticks( yticks )

anim = animation.FuncAnimation( fig, UpdateFrame, \
                                init_func = InitializeFrame, \
                                frames = nSS, \
                                blit = True )

fps = max( 1, nSS / movRunTime )

movName \
  = HOME + 'mov.{:}_multiRun_{:}.mp4'.format( 'AdiabaticCollapse', field )
print( '\n  Making movie' )
print( '  ------------' )
anim.save( movName, fps = fps, dpi = 300 )
print( '\n  Saved {:}'.format( movName ) )

import os
os.system( 'rm -rf __pycache__ ' )
