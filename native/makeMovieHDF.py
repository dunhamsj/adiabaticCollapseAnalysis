#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

from ReadFieldsHDF import ReadFieldsHDF

# --- Define root path for data ---

RootPath \
  = '/home/kkadoogan/Work/Codes/thornado/SandBox/AdiabaticCollapse_XCFC/'
RootPath += 'Output/'

#RootPath = '/lump/data/development/adiabaticCollapse_XCFC/'
#RootPath += 'adiabaticCollapse_XCFC_drMin0.50km_nX512/'

FigTitle = 'AdiabaticCollapse_XCFC'

Fields           = np.array( [ 'AF_T' ] )
Scales           = np.array( [ 1.0 ], np.float64 )
UseSemiLogYScale = True
SnapshotRange    = [0,3001]
PlotEvery        = 1
PlotCellAverage  = True
nNodes           = 2
RunTime          = 10.0 # seconds

rhoMax     = 6.213e14 # g/cc
indDecades = [ 605, 2072, 2332, 2395, 2412 ]

tb = 2.418e2

############################

nFields = Fields.shape[0]

nFiles = SnapshotRange[1] - SnapshotRange[0]

Snapshots \
  = np.linspace( SnapshotRange[0], SnapshotRange[1], nFiles+1, \
                 dtype = np.int64 )[::PlotEvery]

nFiles = Snapshots.shape[0]
Snapshots[0 ] = SnapshotRange[0]
Snapshots[-1] = SnapshotRange[1]

# --- Define where to look for data ---

PathToData = RootPath + 'AdiabaticCollapse_XCFC'

fieldsName = ''
for i in range( nFields ):
  fieldsName += '_' + Fields[i]

SaveFileAs = 'mov.{:}{:}.mp4'.format( FigTitle, fieldsName )

Names = ReadFieldsHDF( PathToData, Snapshots, 'SPHERICAL', True )
Time  = Names['Time'][1]
nSS = Time.shape[0]

x1    = np.array( Names['X1'][1] )
x1lim = ( np.min(x1), np.max(x1) )

x1q = Names['X1'][1]
nX1 = x1q.shape[0] // nNodes

def computeCellAverage( Names, nNodes, Field, nSS ):

  x1_C = np.empty( nX1, np.float64 )

  uh = Names[Field][1]

  if nNodes == 2:
    wq = np.array( [ 0.5, 0.5 ], np.float64 )
  else:
    exit( 'Not available for nNodes = {:}'.format( nNodes ) )

  SqrtGm = Names['GF_Sg'][1]

  uK = np.empty( (nSS,nX1), np.float64 )

  for iSS in range( nSS ):
    for iX1 in range( nX1 ):

      iLo = nNodes * iX1
      iHi = iLo + nNodes

      vK = np.sum( wq * SqrtGm[iSS,0,0,iLo:iHi] )

      uK[iSS,iX1] \
        = np.sum( wq * uh[iSS,0,0,iLo:iHi] * SqrtGm[iSS,0,0,iLo:iHi] ) / vK

      if iSS == 0:
        x1_C[iX1] = np.sum( wq * x1q[iLo:iHi] )

  return uK, x1_C

uK = np.empty( (nFields,nSS,nX1), np.float64 )
for iF in range( nFields ):
  uK[iF], x1_C \
    = computeCellAverage( Names, nNodes, Fields[iF], nSS )
  uK[iF] /= Scales[iF]

header  = 'data[0,1:]  = X1_C [km]\n'
header += 'data[1:,0]  = Time [ms]\n'
header += 'data[1:,1:] = T [K]'

uKK = np.empty( (nSS+1,nX1+1), np.float64 )
uKK[0,0 ] = np.nan
uKK[0,1:] = x1_C
uKK[1:,0] = Time
uKK[1:,1:] = uK[0]

np.savetxt( 'adiabaticCollapse_XCFC_native_{:}.dat'.format( Fields[0] ), \
            uKK, header = header )
exit()

# --- Plotting ---

# Animation program adapted from
# https://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/

fig, ax = plt.subplots( figsize = (8,6) )
fig.suptitle( FigTitle, fontsize = 20 )
ax.grid()

ax.set_xlim( x1lim )
ylim = [ uK.min(), uK.max() ]
ax.set_ylim( ylim  )

ax.set_xlabel( 'Radial Coordinate [km]' )
#ax.set_ylabel( '{:}'.format( Field ) )

if UseSemiLogYScale:
  if( ylim[0] < 0.0 ):
      ax.set_yscale( 'symlog' )
  else:
      ax.set_yscale( 'log' )

ax.set_xscale( 'log' )

xRef = [ 4.0e3, 2.0e3, 1.0e3, 5.0e2, 1.0e2, 5.0e1 ]
for xx in xRef:
    ax.axvline( xx, color = 'b' )

lines = np.empty( nFields, object )
for i in range( nFields ):
  lines[i], = ax.plot( [], [], '.', label = Fields[i] )

ax.legend()

time_text = plt.text( 0.2, 0.8, '', transform = ax.transAxes )

# Intialize each new frame

def InitializeFrame():
  ret = []
  for i in range( nFields ):
    lines[i].set_data([],[])
    ret.append( lines[i] )
  time_text.set_text('')
  ret.append( time_text )
  return ( ret )

# Animation function

def UpdateFrame(t):
  ret = []
  for i in range( nFields ):
    lines[i].set_data( x1_C, uK[i,t] )
    ret.append( lines[i] )
  time_text.set_text( r'$t-t_{{b}}={:.3e}\ \left[\mathrm{{ms}}\right]$' \
                      .format( Time[t] - tb ) )
  ret.append( time_text )
  return ( ret )

# Call the animator

anim = animation.FuncAnimation \
         ( fig, \
           UpdateFrame, \
           init_func = InitializeFrame, \
           frames    = nFiles, \
           blit      = True )

print( '\n    Saving movie {:}...'.format( SaveFileAs ) )

fps = max( 1, np.int64( nFiles / RunTime ) )

anim.save( SaveFileAs, fps = fps )

os.system( 'rm -f *.pyc' )
os.system( 'rm -rf __pycache__' )
