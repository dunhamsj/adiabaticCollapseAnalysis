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

# ID to be used for naming purposes
ID = 'AdiabaticCollapse_XCFC'

HOME = '/home/kkadoogan/'

# Directory containing AMReX plotfiles
plotfileDirectory \
  = HOME + 'Work/Codes/thornado/SandBox/AMReX/Applications/' \
             + 'AdiabaticCollapse_XCFC/'

# plotfile base name (e.g., Advection1D.plt######## -> Advection1D.plt )
plotfileBaseName = ID + '.plt'

# Field to plot
field = 'AF_T'
yLabel = r'$T\ \left[\mathrm{K}\right]$'

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

# Include initial conditions in movie?
showIC = False

plotMesh = False

verbose = True

useCustomLimits = False
ymin = 0.0
ymax = 2.0

movRunTime = 10.0 # seconds

#### ====== End of User Input =======

dataDirectory = '.{:}'.format( ID )

# Append "/" if not present
if not plotfileDirectory[-1] == '/': plotfileDirectory += '/'
if not dataDirectory    [-1] == '/': dataDirectory     += '/'

plotfileArray \
  = MakeDataFile( field, plotfileDirectory, dataDirectory, \
                  plotfileBaseName, 'spherical', \
                  SSi = SSi, SSf = SSf, nSS = nSS, \
                  UsePhysicalUnits = True, \
                  MaxLevel = maxLevel, Verbose = verbose )
plotfileArray = np.copy( plotfileArray[::plotEvery] )

def f(t):

    fileDirectory = dataDirectory + plotfileArray[t] + '/'

    timeFile = fileDirectory + '{:}.dat'.format( 'Time' )
    X1File   = fileDirectory + '{:}.dat'.format( 'X1' )
    dX1File  = fileDirectory + '{:}.dat'.format( 'dX1' )
    dataFile = fileDirectory + '{:}.dat'.format( field )

    dataShape, dataUnits, minVal, maxVal = ReadHeader( dataFile )

    time = np.loadtxt( timeFile )
    X1_C = np.loadtxt( X1File   )
    dX1  = np.loadtxt( dX1File  )
    data = np.loadtxt( dataFile )

    return data, dataUnits, X1_C, dX1, time

data0, dataUnits, X1_C0, dX10, time = f(0)

xL = X1_C0[0 ] - 0.5 * dX10[0 ]
xH = X1_C0[-1] + 0.5 * dX10[-1]

if nSS < 0: nSS = plotfileArray.shape[0]

fig, ax = plt.figure( 1, 1 )
ax.set_title( r'$\texttt{{{:}}}$'.format( ID ), fontsize = 15 )

if not useCustomLimits:
    ymin = +np.inf
    ymax = -np.inf
    for j in range( nSS ):
        dataFile \
          = dataDirectory + plotfileArray[j] + '/{:}.dat'.format( field )
        dataShape, dataUnits, minVal, maxVal = ReadHeader( dataFile )
        ymin = min( ymin, minVal )
        ymax = max( ymax, maxVal )

time_text = ax.text( 0.1, 0.9, '', transform = ax.transAxes, fontsize = 13 )

ax.set_xlabel( r'$r\ \left[\mathrm{km}\right]$', fontsize = 15 )
ax.set_ylabel( yLabel )

ax.set_xlim( xL + 0.25 * dX10[0], xH )
ax.set_ylim( ymin, ymax )

ax.grid( which = 'both' )

if useLogScale_Y: ax.set_yscale( 'log' )
ax.set_xscale( 'log' )

if plotMesh: mesh, = ax.plot( [],[], 'b.', label = 'mesh boundaries'    )
if showIC: IC,     = ax.plot( [],[], 'r-', label = r'$u\left(0\right)$' )
line,              = ax.plot( [],[], 'k-', label = r'$u\left(t\right)$' )

def InitializeFrame():

    line.set_data([],[])
    time_text.set_text('')
    if showIC:   IC  .set_data([],[])
    if plotMesh: mesh.set_data([],[])

    if showIC and plotMesh: ret = ( line, time_text, IC, mesh )
    elif showIC:            ret = ( line, time_text, IC )
    elif plotMesh:          ret = ( line, time_text, mesh )
    else:                   ret = ( line, time_text )

    return ret

def UpdateFrame( t ):

    print('    {:}/{:}'.format( t, nSS ) )
    data, dataUnits, X1_C, dX1, time = f(t)

    time_text.set_text( r'$t={:.3e}\ \left[\mathrm{{ms}}\right]$' \
                        .format( time ) )

    line             .set_data( X1_C , data .flatten() )
    if showIC:   IC  .set_data( X1_C0, data0.flatten() )
    if plotMesh: mesh.set_data( X1_C - 0.5 * dX1, 0.5 * ( ymin + ymax ) )

    if showIC and plotMesh: ret = ( line, time_text, IC, mesh )
    elif showIC:            ret = ( line, time_text, IC )
    elif plotMesh:          ret = ( line, time_text, mesh )
    else:                   ret = ( line, time_text )

    return ret

ax.legend( prop = {'size':12} )

xRef = [ 4.0e3, 2.0e3, 1.0e3, 5.0e2, 1.0e2, 5.0e1 ]
for xx in xRef:
    ax.axvline( xx, color = 'b', alpha = 0.3 )

anim = animation.FuncAnimation( fig, UpdateFrame, \
                                init_func = InitializeFrame, \
                                frames = nSS, \
                                blit = True )

fps = max( 1, nSS / movRunTime )

movName = 'mov.{:}_{:}.mp4'.format( ID, field )
print( '\n  Making movie' )
print( '  ------------' )
anim.save( movName, fps = fps, dpi = 300 )
print( '\n  Saved {:}'.format( movName ) )

import os
os.system( 'rm -rf __pycache__ ' )
