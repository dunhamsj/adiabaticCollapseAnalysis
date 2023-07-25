#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from UtilitiesModule import GetData, GetFileArray

ID = 'AdiabaticCollapse_XCFC'

plotfileDirectory \
  = '/home/kkadoogan/Work/Codes/thornado/SandBox/AMReX/' \
      + 'Applications/{:}/{:}/'.format( ID, ID )
plotfileBaseName = ID + '.plt'

saveFig = True
saveFigAs \
  = '/home/kkadoogan/fig.AdibaticCollapse_XCFC_MultiPanel_Collapse.png'

snapshots = np.array( [ 630, 2144, 2413, 2479, 2497 ], dtype = np.int64 )

rhomax = 5.203e+14 # g/cm^3
tb     = 2.503e+02 # ms
indMax = 2503

# colorblind-friendly palette: https://gist.github.com/thriveth/8560036
color = ['#377eb8', '#ff7f00', '#4daf4a', \
         '#f781bf', '#a65628', '#984ea3', \
         '#999999', '#e41a1c', '#dede00']

plotfileArray \
  = GetFileArray( plotfileDirectory, plotfileBaseName )

fig, axs = plt.subplots( 2, 2 )

plotFields = 'micro'

for iSS in range( snapshots.shape[0] ):

    if plotFields == 'hydro':

        D, DataUnit, X1, X2, X3, dX1, dX2, dX3, xL, xU, nX, Time \
          = GetData( plotfileDirectory, plotfileBaseName, 'PF_D', \
                     'spherical', True, \
                     argv = ['x',str( plotfileArray[snapshots[iSS]] )], \
                     MaxLevel = -1, \
                     ReturnTime = True, ReturnMesh = True, Verbose = False )
        X1 = np.copy( X1[:,0,0] )

        D = np.copy( D[:,0,0] )
        axs[0,0].semilogy( X1, D, c = color[iSS] )

        V1, DataUnit, \
          = GetData( plotfileDirectory, plotfileBaseName, 'PF_V1', \
                     'spherical', True, \
                     argv = ['x',str( plotfileArray[snapshots[iSS]] )], \
                     MaxLevel = -1, \
                     ReturnTime = False, ReturnMesh = False, Verbose = False )
        V1 = np.copy( V1[:,0,0] )
        axs[0,1].plot( X1, V1 / 2.99792458e5, c = color[iSS] )

        Psi, DataUnit, \
          = GetData( plotfileDirectory, plotfileBaseName, 'GF_Psi', \
                     'spherical', True, \
                     argv = ['x',str( plotfileArray[snapshots[iSS]] )], \
                     MaxLevel = -1, \
                     ReturnTime = False, ReturnMesh = False, Verbose = False )
        Psi = np.copy( Psi[:,0,0] )
        if iSS == snapshots.shape[0]-1:
            axs[1,0].plot( X1, Psi, ls = '-', c = color[iSS], label = r'$\psi$' )
        else:
            axs[1,0].plot( X1, Psi, ls = '-', c = color[iSS] )

        Alpha, DataUnit, \
          = GetData( plotfileDirectory, plotfileBaseName, 'GF_Alpha', \
                     'spherical', True, \
                     argv = ['x',str( plotfileArray[snapshots[iSS]] )], \
                     MaxLevel = -1, \
                     ReturnTime = False, ReturnMesh = False, Verbose = False )
        Alpha = np.copy( Alpha[:,0,0] )
        if iSS == snapshots.shape[0]-1:
            axs[1,0].plot( X1, Alpha, ls = '--', \
                           c = color[iSS], label = r'$\alpha$' )
        else:
            axs[1,0].plot( X1, Alpha, ls = '--', c = color[iSS] )

        T, DataUnit, \
          = GetData( plotfileDirectory, plotfileBaseName, 'AF_T', \
                     'spherical', True, \
                     argv = ['x',str( plotfileArray[snapshots[iSS]] )], \
                     MaxLevel = -1, \
                     ReturnTime = False, ReturnMesh = False, Verbose = False )
        T = np.copy( T[:,0,0] )
        axs[1,1].semilogy( X1, T, c = color[iSS] )

    elif plotFields == 'micro':

        D, DataUnit, X1, X2, X3, dX1, dX2, dX3, xL, xU, nX, Time \
          = GetData( plotfileDirectory, plotfileBaseName, 'PF_D', \
                     'spherical', True, \
                     argv = ['x',str( plotfileArray[snapshots[iSS]] )], \
                     MaxLevel = -1, \
                     ReturnTime = True, ReturnMesh = True, Verbose = False )
        X1 = np.copy( X1[:,0,0] )

        D = np.copy( D[:,0,0] )
        axs[0,0].semilogy( X1, D, c = color[iSS] )

        T, DataUnit \
          = GetData( plotfileDirectory, plotfileBaseName, 'AF_T', \
                     'spherical', True, \
                     argv = ['x',str( plotfileArray[snapshots[iSS]] )], \
                     MaxLevel = -1, \
                     ReturnTime = False, ReturnMesh = False, Verbose = False )

        T = np.copy( T[:,0,0] )
        axs[0,1].semilogy( X1, T, c = color[iSS] )

        Ye, DataUnit, \
          = GetData( plotfileDirectory, plotfileBaseName, 'AF_Ye', \
                     'spherical', True, \
                     argv = ['x',str( plotfileArray[snapshots[iSS]] )], \
                     MaxLevel = -1, \
                     ReturnTime = False, ReturnMesh = False, Verbose = False )
        Ye = np.copy( Ye[:,0,0] )
        axs[1,0].plot( X1, Ye, c = color[iSS] )

        S, DataUnit, \
          = GetData( plotfileDirectory, plotfileBaseName, 'AF_S', \
                     'spherical', True, \
                     argv = ['x',str( plotfileArray[snapshots[iSS]] )], \
                     MaxLevel = -1, \
                     ReturnTime = False, ReturnMesh = False, Verbose = False )
        S = np.copy( S[:,0,0] )
        axs[1,1].plot( X1, S, c = color[iSS] )

xRef = [ 4.0e3, 2.0e3, 1.0e3, 5.0e2, 1.0e2, 5.0e1 ]
for i in range( 2 ):
    for j in range( 2 ):
        for xx in xRef:
            axs[i,j].axvline( xx, color = 'b', alpha = 0.3 )

if plotFields == 'hydro':
    axs[1,0].legend()
    axs[0,0].set_ylabel( r'$\rho\ \left[\mathrm{g}\,\mathrm{cm}^{-3}\right]$' )
    axs[0,1].set_ylabel( r'$v/c$' )
    axs[1,1].set_ylabel( r'$T\ \left[\mathrm{K}\right]$' )
elif plotFields == 'micro':
    axs[0,0].set_ylabel( r'$\rho\ \left[\mathrm{g}\,\mathrm{cm}^{-3}\right]$' )
    axs[0,1].set_ylabel( r'$T\ \left[\mathrm{K}\right]$' )
    axs[1,0].set_ylabel( r'$Y_{e}$' )
    axs[1,1].set_ylabel( r'$S\ \left[\mathrm{k}_{\mathrm{B}}/\mathrm{baryon}\right]$' )

axs[0,0].xaxis.set_tick_params \
  ( which = 'both',top = True, left = True , bottom = True, right = False )
axs[0,1].xaxis.set_tick_params \
  ( which = 'both', top = True, left = False, bottom = True, right = True  )
axs[1,0].xaxis.set_tick_params \
  ( which = 'both', top = True, left = True , bottom = True, right = False )
axs[1,1].xaxis.set_tick_params \
  ( which = 'both', top = True, left = False, bottom = True, right = True  )

axs[0,1].yaxis.set_label_position( 'right' )
axs[0,1].yaxis.tick_right()
axs[1,1].yaxis.set_label_position( 'right' )
axs[1,1].yaxis.tick_right()

xticks = [ 1.0e0, 1.0e1, 1.0e2, 1.0e3 ]
xticklabels = [ r'$10^{0}$', r'$10^{1}$', r'$10^{2}$', r'$10^{3}$' ]

for i in range( axs.shape[0] ):
    for j in range( axs.shape[1] ):
        axs[i,j].set_xlim( 0.0 + 0.25 * dX1[0], 8.0e3 + 1.0e3 )
        axs[i,j].set_xscale( 'log' )
#        axs[i,j].grid( axis = 'x')#, which = 'both' )
        axs[i,j].set_xticks( xticks )

axs[0,0].set_xticklabels( '' )
axs[0,1].set_xticklabels( '' )
axs[1,0].set_xticklabels( xticklabels )
axs[1,1].set_xticklabels( xticklabels )

fig.suptitle( 'Adiabatic Collapse, AMReX, Multi-Level,\nCollapse Phase' )
fig.supxlabel( r'$r/\mathrm{km}$', y = 0.025 )
plt.subplots_adjust( hspace = 0, wspace = 0 )

if saveFig:
  plt.savefig( saveFigAs, dpi = 300 )
  print( '\n  Saved {:}'.format( saveFigAs ) )
else:
  plt.show()

import os
os.system( 'rm -rf __pycache__ ' )
