#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

from Conservation import Conservation

Root = '/Users/dunhamsj/Desktop/AdiabaticCollapse_XCFC/'

nNodes = 2

Snapshots = np.linspace( 0, 3001, 3002, dtype = np.int64 )

nRows = 1
nCols = 1

fig, ax = plt.subplots( nRows, nCols, figsize = (8,6) )

def MakePlot( ax, C, c, ls, lab = '' ):

    MADM = C.MADM * C.BethePerSolarMass
    OGM  = C.OGM  * C.BethePerSolarMass

    a = C.names['GF_al'][1][:,0,0,0]

    C.PlotLine( ax, a, ( MADM - OGM ) - ( MADM[0] - OGM[0] ), \
                c = c, ls = ls, label = lab )

    return a.min(), a.max()

xLo = +np.inf
xHi = -np.inf

DataDirectory = Root + 'AdiabaticCollapse_XCFC_nX256_drMin1.00km/'
C = Conservation( DataDirectory, nNodes, Snapshots )
amin, amax = MakePlot( ax, C, c = 'k', ls = '-', lab = 'nX=256, drMin=1.00km' )
xLo = min( xLo, amin )
xHi = max( xHi, amax )
del C

DataDirectory = Root + 'AdiabaticCollapse_XCFC_nX512_drMin1.00km/'
C = Conservation( DataDirectory, nNodes, Snapshots )
amin, amax = MakePlot( ax, C, c = 'r', ls = '-', lab = 'nX=512, drMin=1.00km' )
xLo = min( xLo, amin )
xHi = max( xHi, amax )
del C

DataDirectory = Root + 'AdiabaticCollapse_XCFC_nX256_drMin0.50km/'
C = Conservation( DataDirectory, nNodes, Snapshots )
amin, amax = MakePlot( ax, C, c = 'k', ls = '--', lab = 'nX=256, drMin=0.50km' )
xLo = min( xLo, amin )
xHi = max( xHi, amax )
del C

DataDirectory = Root + 'AdiabaticCollapse_XCFC_nX512_drMin0.50km/'
C = Conservation( DataDirectory, nNodes, Snapshots )
amin, amax = MakePlot( ax, C, c = 'r', ls = '--', lab = 'nX=512, drMin=0.50km' )
xLo = min( xLo, amin )
xHi = max( xHi, amax )
del C

ax.set_xlim( xLo, xHi )

ax.set_xlabel( r'$\alpha_{C}$' )

ax.legend()
ax.set_ylabel( r'$E_{ADM}-M_{OG}$ [B]' )

plt.savefig( 'fig.Conservation_CentralLapse.png', dpi = 300 )
#plt.show()
plt.close()

#DataDirectory = Root + 'AdiabaticCollapse_XCFC_nX256_drMin1.00km/'
#C = Conservation( DataDirectory, nNodes, Snapshots )
#
#r  = C.names['X1'][1]
#t  = C.names['Time'][1]
#al = C.names['GF_al'][1][:,0,0,:]
#
#tLo = t.min()
#tHi = t.max()
#rLo = r.min()
#rHi = r.max()
#
#plt.imshow( al, \
#            extent = [ rLo, rHi, tLo, tHi ], \
#            aspect = 'auto', \
#            origin = 'lower' )
#plt.colorbar()
#plt.show()
#plt.close()

import os
os.system( 'rm -rf __pycache__' )
