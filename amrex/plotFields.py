#!/usr/bin/env python3

import numpy as np
from sys import argv
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from UtilitiesModule import GetData, GetNorm

#### ========== User Input ==========

# Specify name of problem
problemName = 'AdiabaticCollapse_XCFC'

# Specify title of figure
figTitle = problemName

# Specify directory containing plotfiles
plotfileDirectory \
  = [ '/home/kkadoogan/Work/Codes/thornado/SandBox/AMReX/Applications/' \
      + '{:}/'.format( problemName ) ]
label \
  = [ 'lab' ]

# Specify plot file base name
plotfileBaseName = problemName + '.plt'

# Specify field to plot
field = 'AF_T'
yLabel = r'$T\,\left[\mathrm{K}\right]$'

# Specify to plot in log-scale
useLogYScale = True

maxLevel = -1

verbose = True

saveFig = False

#### ====== End of User Input =======

nRuns = len( plotfileDirectory )

FigName = 'fig.{:}_{:}.png'.format( problemName, field )

# Append "/" to plotfileDirectory, if not present
for i in range( nRuns ):
    if( not plotfileDirectory[i][-1] == '/' ): plotfileDirectory[i] += '/'

Data     = np.empty( nRuns, object )
DataUnit = np.empty( nRuns, object )
X1       = np.empty( nRuns, object )
X2       = np.empty( nRuns, object )
X3       = np.empty( nRuns, object )
dX1      = np.empty( nRuns, object )
dX2      = np.empty( nRuns, object )
dX3      = np.empty( nRuns, object )
xL       = np.empty( nRuns, object )
xH       = np.empty( nRuns, object )
nX       = np.empty( nRuns, object )
Time     = np.empty( nRuns, object )

for i in range( nRuns ):

    Data[i], DataUnit[i], X1[i], X2[i], X3[i], dX1[i], dX2[i], dX3[i], \
    xL[i], xH[i], nX[i], Time[i] \
      = GetData( plotfileDirectory[i], plotfileBaseName, field, \
                 'spherical', False, argv = argv, \
                 MaxLevel = maxLevel, \
                 ReturnTime = True, ReturnMesh = True, Verbose = verbose )

fig, ax = plt.subplots( 1, 1 )

for i in range( nRuns ):
    ax.plot( X1[i][:,0,0], Data[i][:,0,0], \
             '.', markersize = 5)#, label = label[i] )

#ax.legend()

if( useLogYScale ): ax.set_yscale( 'log' )
ax.set_xscale( 'log' )

ax.set_xlabel( r'$r\,\left[\mathrm{km}\right]$' )
ax.set_ylabel( yLabel )

xRef = [ 5.0e1, 1.0e2, 5.0e2, 1.0e3, 2.0e3, 4.0e3 ]
for xx in xRef:
    ax.axvline( xx, color = 'k' )

if saveFig:

    plt.saveFig( FigName, dpi = 300 )

else:

    plt.show()
    plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
