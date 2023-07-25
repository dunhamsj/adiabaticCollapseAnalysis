#!/usr/bin/env python3

import numpy as np
from sys import argv
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from UtilitiesModule import GetData, GetNorm

#### ========== User Input ==========

# Specify name of problem
ProblemName = 'AdiabaticCollapse_XCFC'

# Specify title of figure
FigTitle = ProblemName

# Specify directory containing plotfiles
PlotFileDirectory = np.array( [ \
#'/lump/data/development/adiabaticCollapse_XCFC/\
#adiabaticCollapse_XCFC_UniGrid_NoGravitySolve/', \
'/home/kkadoogan/Work/Codes/thornado/SandBox/AMReX/Applications/\
AdiabaticCollapse_XCFC/' ], str )

# Specify plot file base name
PlotFileBaseName = ProblemName + '.plt'

# Specify field to plot
Field = 'AF_T'

# Specify to plot in log-scale
UseLogScale = True

# Specify whether or not to use physical units
UsePhysicalUnits = True

# Specify coordinate system (currently supports 'cartesian' and 'spherical')
CoordinateSystem = 'spherical'

MaxLevel = -1

Verbose = True

UseCustomLimits = False
vmin = 0.0
vmax = 2.0

SaveFig = False

#### ====== End of User Input =======

nRuns = PlotFileDirectory.shape[0]

ID      = '{:s}_{:s}'.format( ProblemName, Field )
FigName = 'fig.{:s}.png'.format( ID )

# Append "/" to PlotFileDirectory, if not present
for i in range( PlotFileDirectory.shape[0] ):
    if( not PlotFileDirectory[i][-1] == '/' ): PlotFileDirectory[i] += '/'

TimeUnit   = ''
LengthUnit = ''
if( UsePhysicalUnits ):

    TimeUnit   = 'ms'
    LengthUnit = 'km'

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
      = GetData( PlotFileDirectory[i], PlotFileBaseName, Field, \
                 CoordinateSystem, UsePhysicalUnits, argv = argv, \
                 MaxLevel = MaxLevel, \
                 ReturnTime = True, ReturnMesh = True, Verbose = True )

label = [ 'UniGrid', 'MultiGrid' ]
for i in range( nRuns ):
    plt.plot( X1[i] , Data[i] , '.', markersize = 5)#, label = label[i] )

#plt.legend()
if( UseLogScale ): plt.yscale( 'log' )
plt.xlim( xL[0][0] + 0.5 * dX1[0][0], xH[0][0] - 0.5 * dX1[0][0] )
#plt.xlim( 45.0, 105.0 )
plt.xscale( 'log' )
plt.xlabel( 'X1' + ' ' + LengthUnit )
plt.ylabel( Field )

plt.axvline( 4.0e3, color = 'k' )
plt.axvline( 2.0e3, color = 'k' )
plt.axvline( 1.0e3, color = 'k' )
plt.axvline( 5.0e2, color = 'k' )
plt.axvline( 1.0e2, color = 'k' )
plt.axvline( 5.0e1, color = 'k' )
if SaveFig:

    plt.savefig( FigName, dpi = 300 )

else:

    plt.show()
    plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
