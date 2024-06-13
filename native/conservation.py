#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( './Publication.sty' )

from ReadFieldsHDF import ReadFieldsHDF

class Conservation:

    def __init__( self, DataDirectory, nNodes, Snapshots, \
                  xL = 0.0, xR = 8.0e3, \
                  suffix = '' ):

        if DataDirectory[-1] != '/':

            self.DataDirectory = DataDirectory + '{:}/'.format( suffix )

        else:

            self.DataDirectory = DataDirectory[:-1] + '{:}/'.format( suffix )

        self.LengthScale = 1.0e5

        self.nNodes = nNodes

        self.Snapshots = Snapshots

        self.xL = xL * self.LengthScale
        self.xR = xR * self.LengthScale

        if self.nNodes == 2:

            self.wq = np.array( [ 0.5, 0.5 ], np.float64 )

        print( '' )
        print( '  Creating instance of Conservation class:' )
        print( '  ----------------------------------------' )
        print( '    DataDirectory: {:}'.format( DataDirectory ) )
        print( '      LengthScale: {:.1e} km'.format( self.LengthScale ) )
        print( '           nNodes: {:d}'.format( nNodes ) )
        print( '               xL: {:.2e} km'.format( xL ) )
        print( '               xR: {:.2e} km'.format( xR ) )
        print( '' )

        ErgsPerGram      = ( 2.99792458e10 )**2
        SolarMassPerGram = 1.98892e33

        self.BethePerErg       = 1.0e-51
        self.BethePerGram      = ErgsPerGram * self.BethePerErg
        self.BethePerSolarMass = self.BethePerGram * SolarMassPerGram

        self.ind = self.Snapshots
        self.GetTallyData()
        self.GetThornadoData()

        return


    def GetTallyData( self ):

        scale = 4.0 * np.pi / ( 2.0 * np.pi**2 )

        tM, M, OGM, IniM, dM \
          = np.loadtxt( self.DataDirectory \
                          + 'AdiabaticCollapse_XCFC_Tally_BaryonicMass.dat', \
                        skiprows = 1, unpack = True )

        tADM, MADM, OGMADM, IniMADM, dMADM \
          = np.loadtxt( self.DataDirectory \
                          + 'AdiabaticCollapse_XCFC_Tally_ADMMass.dat', \
                        skiprows = 1, unpack = True )

        tE, E, OGE, IniE, dE \
          = np.loadtxt( self.DataDirectory \
                          + 'AdiabaticCollapse_XCFC_Tally_Energy.dat', \
                        skiprows = 1, unpack = True )

        ind = self.ind

        self.tTally = tM[ind]

        self.M    = M   [ind] * scale
        self.OGM  = OGM [ind] * scale
        self.IniM = IniM[ind] * scale
        self.dM   = dM  [ind] * scale

        self.MADM    = MADM   [ind]
        self.OGMADM  = OGMADM [ind]
        self.IniMADM = IniMADM[ind]
        self.dMADM   = dMADM  [ind]

        self.E    = E   [ind] * scale
        self.OGE  = OGE [ind] * scale
        self.IniE = IniE[ind] * scale
        self.dE   = dE  [ind] * scale

        return


    def GetThornadoData( self ):

        self.nFiles = self.Snapshots.shape[0]

        self.names \
          = ReadFieldsHDF( self.DataDirectory + 'AdiabaticCollapse_XCFC', \
                           self.Snapshots, CoordinateSystem = 'SPHERICAL', \
                           UsePhysicalUnits = True, Verbose = True )

        self.nX = np.array( self.names['CF_D'][1].shape[-1] )
        self.nX = np.int64( self.nX / self.nNodes )

        self.tThornado = self.names['Time'][1]

        self.dX = self.names['dX1'][1] * self.LengthScale

        return


    def ComputeIntegral \
          ( self, Field, PsiExponent = 0, Norm = False ):

        SqrtGm = self.names['GF_Sg'][1][:,0,0,:] * self.LengthScale**2 \
                   * self.names['GF_CF'][1][:,0,0,:]**( PsiExponent - 6 )

        Integral = np.zeros( (self.nFiles), np.float64 )

        if Norm:

            Vol = np.zeros( (self.nFiles), np.float64 )

        for iSS in range( self.nFiles ):

            for iX1 in range( self.nX ):

                iLo = iX1*self.nNodes
                iHi = iX1*self.nNodes+self.nNodes

                if Norm:

                    Vol[iSS] \
                      += 4.0 * np.pi * self.dX[iX1] \
                           * np.sum( self.wq * SqrtGm[iSS,iLo:iHi] )

                Integral[iSS] \
                  += 4.0 * np.pi * self.dX[iX1] \
                       * np.sum( self.wq * Field [iSS,iLo:iHi] \
                                         * SqrtGm[iSS,iLo:iHi] )

        if Norm:

            Integral /= Vol

        return Integral


    def PlotLine( self, ax, x, y, c = 'k', ls = '-', label = '' ):

        ax.plot( x, y, c = c, ls = ls, label = label )

        return


if __name__ == '__main__':

    import os
    os.system( 'rm -rf __pycache__' )
