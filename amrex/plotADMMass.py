#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

saveFig = True

rootDirectory \
  = '/home/kkadoogan/Work/Codes/thornado/SandBox/AMReX/Applications/'

ID = 'AdiabaticCollapse_XCFC'

tallyFileDirectory = '{:}{:}/{:}/'.format( rootDirectory, ID, ID )

admTallyFilename  = ID + '.Tally_ADMMass.dat'

t, Eint, EOG, Einit, dE \
  = np.loadtxt( tallyFileDirectory + admTallyFilename, \
                skiprows = 1, unpack = True )
SolarMass = 1.98892e33
c         = 2.99792458e10
Bethe     = SolarMass * c**2 * 1.0 / 1.0e51

Eint_B  = Eint  * Bethe
EOG_B   = EOG   * Bethe
Einit_B = Einit * Bethe
dE_B    = dE    * Bethe

massTallyFilename = ID + '.Tally_BaryonicMass.dat'
t, Mint, MOG, Minit, dM \
  = np.loadtxt( tallyFileDirectory + massTallyFilename, \
                skiprows = 1, unpack = True )

MOG_B = MOG * Bethe

#fig, ax = plt.subplots( 1, 1 )
#
#ax.set_title( 'Adiabatic Collapse_XCFC, AMReX, Multi-Level\nADM Mass Tally' )
#
#ax.plot( t, Eint_B - Einit_B + MOG_B )
#
#ax.set_xlabel( r'$t/\mathrm{ms}$' )
#yLabel = r'$E_{\mathrm{ADM}}\left(t\right)$' \
#         + r'$-E_{\mathrm{ADM}}\left(0\right)$' \
#         + r'$+dE_{\mathrm{baryonic}}$' \
#         + r'$\ \left[\mathrm{B}\right]$'
#ax.set_ylabel( yLabel )
#
#if saveFig:
#    figName = '/home/kkadoogan/fig.ADMMass.png'
#    plt.savefig( figName, dpi = 300 )
#    print( '\n  Saved {:}'.format( figName ) )
#else:
#    plt.show()
#plt.close()

fig, ax = plt.subplots( 1, 1 )

ax.set_title \
  ( 'Adiabatic Collapse_XCFC, AMReX, Multi-Level\nBaryonic Mass Tally' )

ax.plot( t, np.abs( dM ) / Minit )

ax.set_xlabel( r'$t/\mathrm{ms}$' )
yLabel = r'$\left|dM\right|/M\left(0\right)$'
ax.set_ylabel( yLabel )
ax.set_yscale( 'log' )

if saveFig:
    figName = '/home/kkadoogan/fig.BaryonicMass.png'
    plt.savefig( figName, dpi = 300 )
    print( '\n  Saved {:}'.format( figName ) )
else:
    plt.show()
plt.close()
