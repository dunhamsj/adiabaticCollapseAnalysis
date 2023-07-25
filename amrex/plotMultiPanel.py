#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'Publication.sty' )

from UtilitiesModule import GetData, GetFileArray
from MakeDataFile import MakeDataFile, ReadHeader

class MultiPanel:

  def __init__( self, plotFileDirectory, \
                      snapShots = np.array( [ -1 ], np.int64 ) ):

    self.plotFileDirectory = plotFileDirectory
    self.plotFileBaseName = 'AdiabaticCollapse_XCFC.plt_'
    self.snapShots = snapShots

    return

  def GetData( self, Field ):

    plotFileArray \
      = GetFileArray( self.plotFileDirectory, self.plotFileBaseName )

    for iSS in range( self.snapShots.shape[0] ):

      Data, DataUnit, X1, X2, X3, dX1, dX2, dX3, xL, xU, nX, Time \
        = GetData( self.plotFileDirectory, self.plotFileBaseName, Field, \
                   'spherical', True, \
                   argv = ['x',str( plotFileArray[self.snapShots[iSS]] )], \
                   MaxLevel = -1, \
                   ReturnTime = True, ReturnMesh = True, Verbose = False )

    return Data, DataUnit, X1, dX1, xL, xU, Time

if __name__ == '__main__':

  Snapshots = [ 631, 2144, 2413, 2479, 2479, 3001 ]

  indMax = 2503
  rhoMax = 4.865e14 # g/cm^3
  tb = 2.503e2

  saveFig = False
  saveFigAs = 'fig.AdibaticCollapse_XCFC_MultiPanel.png'

  plotFileDirectory \
    = '/lump/data/development/gravitationalCollapse/adiabaticCollapse_XCFC/'

  MPf \
    = MultiPanel \
        ( plotFileDirectory, snapShots = np.array( [ -1 ], np.int64 ) )

  PF_D , unit_PF_D , X1, dX1, xL, xU, Time = MPf.GetData( 'PF_D'      )
  GF_b1, unit_GF_b1, X1, dX1, xL, xU, Time = MPf.GetData( 'GF_Beta_1' )
  PF_V1, unit_PF_V1, X1, dX1, xL, xU, Time = MPf.GetData( 'PF_V1'     )
  AF_P , unit_AF_P , X1, dX1, xL, xU, Time = MPf.GetData( 'AF_P'      )
  GF_CF, unit_GF_CF, X1, dX1, xL, xU, Time = MPf.GetData( 'GF_Psi'    )
  GF_Al, unit_GF_Al, X1, dX1, xL, xU, Time = MPf.GetData( 'GF_Alpha'  )

  fig, axs = plt.subplots( 2, 2, figsize = ( 12,9 ) )
  fig.suptitle( 'Adiabatic Collapse (XCFC)\nTime: {:.3e} ms'.format( Time ) )

  for i in range( 2 ):
    for j in range( 2 ):
      axs[i,j].set_xlim( xL[0] + 0.1, xU[0] )
      axs[i,j].set_xscale( 'log')
      axs[i,j].grid()
      axs[i,j].set_xlabel( 'Radial Coordinate [km]' )

  axs[0,0].semilogy( X1, PF_D )
  axs[0,0].set_ylabel( 'PF_D ' + unit_PF_D )
  axs[0,1].plot    ( X1, GF_b1 / 2.99792458e5, label = r'$\beta^{1}/c$' )
  axs[0,1].plot    ( X1, PF_V1 / 2.99792458e5, label = r'$v^{1}/c$' )
  axs[0,1].legend()
  axs[1,0].semilogy( X1, AF_P )
  axs[1,0].set_ylabel( 'AF_P ' + unit_AF_P )
  axs[1,1].plot    ( X1, GF_CF, label = r'$\psi$' )
  axs[1,1].plot    ( X1, GF_Al, label = r'$\alpha$' )
  axs[1,1].legend()

  if saveFig:
    plt.savefig( saveFigAs, dpi = 300, bbox_inches = 'tight' )
  else:
    plt.show()

  import os
  os.system( 'rm -rf __pycache__ ' )
