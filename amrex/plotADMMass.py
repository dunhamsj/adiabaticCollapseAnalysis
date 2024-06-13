#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

saveFig = False

tb = 2.530e2

ID = [ 'AdiabaticCollapse_XCFC' ]
lab = [ 'old' ]
nRuns = len( ID )

rootDirectory = '/home/kkadoogan/'
plotfileDirectory = [ rootDirectory + '{:}/'.format( IDD ) for IDD in ID ]

tallyFileDirectory \
  = [ '{:}'.format( plotfileDirectory[i] ) for i in range( nRuns ) ]

admTallyFilename  = [ IDD + '.Tally_ADMMass.dat'      for IDD in ID ]
massTallyFilename = [ IDD + '.Tally_BaryonicMass.dat' for IDD in ID ]

SolarMass = 1.98892e33
c         = 2.99792458e10
Bethe     = SolarMass * c**2 * 1.0 / 1.0e51

fig, ax = plt.subplots( 1, 1 )
ax.set_title( 'Adiabatic Collapse, AMReX, Multi-Level\nADM Mass Tally' )

ax.set_xlabel( r'$\left(t-t_{b}\right)/\mathrm{ms}$' )
yLabel = r'$E_{\mathrm{ADM}}\left(t\right)$' \
         + r'$-E_{\mathrm{ADM}}\left(0\right)$' \
         + r'$+dE_{\mathrm{baryonic}}$' \
         + r'$\ \left[\mathrm{B}\right]$'
ax.set_ylabel( yLabel )

for i in range( nRuns ):

    t, Eint, EOG, Einit, dE \
      = np.loadtxt( tallyFileDirectory[i] + admTallyFilename[i], \
                    skiprows = 1, unpack = True )

    ind = np.where( t < 6.80e2 )[0]

    Eint_B  = Eint  * Bethe
    EOG_B   = EOG   * Bethe
    Einit_B = Einit * Bethe
    dE_B    = dE    * Bethe

    t, Mint, MOG, Minit, dM \
      = np.loadtxt( tallyFileDirectory[i] + massTallyFilename[i], \
                    skiprows = 1, unpack = True )

    MOG_B = MOG * 2.0 / np.pi * Bethe

    ax.plot( t[ind] - tb, \
             Eint_B[ind] - Einit_B[ind] + MOG_B[ind], label = lab[i] )

ax.legend()
ax.grid()
if saveFig:
    figName = '/home/kkadoogan/fig.ADMMass.png'
    plt.savefig( figName, dpi = 300 )
    print( '\n  Saved {:}'.format( figName ) )
else:
    plt.show()
plt.close()

fig, ax = plt.subplots( 1, 1 )
ax.set_title \
  ( 'Adiabatic Collapse, AMReX, Multi-Level\nBaryonic Mass Tally' )

ax.set_xlabel( r'$\left(t-t_{b}\right)/\mathrm{ms}$' )
yLabel = r'$\left|dM\right|/M\left(0\right)$'
ax.set_ylabel( yLabel )
ax.set_yscale( 'log' )

for i in range( nRuns ):

    t, Mint, MOG, Minit, dM \
      = np.loadtxt( tallyFileDirectory[i] + massTallyFilename[i], \
                    skiprows = 1, unpack = True )

    ind = np.where( t < 6.80e2 )[0]

    ax.plot( t[ind] - tb, np.abs( dM[ind] ) / Minit[ind], label = lab[i] )

ax.legend()
ax.grid()
if saveFig:
    figName = '/home/kkadoogan/fig.BaryonicMass.png'
    plt.savefig( figName, dpi = 300 )
    print( '\n  Saved {:}'.format( figName ) )
else:
    plt.show()
plt.close()
