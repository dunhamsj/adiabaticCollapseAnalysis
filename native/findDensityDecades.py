#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

from ReadFieldsHDF import ReadFieldsHDF

class DensityDecades:

    def __init__( self, DataDirectory, iLo, iHi ):

        self.DataDirectory = DataDirectory
        self.iLo = iLo
        self.iHi = iHi
        self.nFiles = iHi - iLo + 1
        self.Snapshots \
          = np.linspace( self.iLo, self.iHi, self.nFiles, dtype = np.int64 )

        return

    def GetData( self ):

        names \
          = ReadFieldsHDF \
              ( PathToData = self.DataDirectory + 'AdiabaticCollapse_XCFC', \
                Snapshots = self.Snapshots, \
                CoordinateSystem = 'SPHERICAL', \
                UsePhysicalUnits = True, \
                Verbose = True )

        self.nX = names['X1_C'][1].shape[0]

        self.nNodes = np.int64( names['X1'][1].shape[0] / self.nX )

        self.PF_D = names['PF_D'][1][:,0,0,0]

        self.Time = names['Time'][1]

        return

    def FindDensityDecades( self ):

        self.DensityDecades = np.logspace( 10, 15, 6 )
        self.FoundDecade    \
          = np.array( [ False, False, False, False, False, False ], bool )

        self.ind = np.empty( (self.DensityDecades.shape[0]), np.int64 )
        self.t   = np.empty( (self.DensityDecades.shape[0]), np.int64 )

        Density    = 0.0
        MaxDensity = 0.0
        tMax       = 0.0
        indMax     = 0

        for iSS in range( self.nFiles ):

            Density = self.PF_D[iSS]

            if Density > MaxDensity:

                MaxDensity = Density
                tMax       = self.Time[iSS]
                indMax     = iSS

            for iDec in range( self.DensityDecades.shape[0] ):

                if Density > self.DensityDecades[iDec] \
                     and not self.FoundDecade[iDec]:

                    self.FoundDecade[iDec] = True
                    self.ind        [iDec] = iSS
                    self.t          [iDec] = self.Time[iSS]

        print( self.ind )
        print( 'MaxDensity: {:.3e} g/cm^3'.format( MaxDensity ) )
        print( '      tMax: {:.3e} ms'.format( tMax ) )
        print( '    indMax: {:d}'.format( indMax ) )

        self.MaxDensity = MaxDensity
        self.tMax       = tMax
        self.indMax     = indMax

if __name__ == '__main__':

    Root = '/home/kkadoogan/Work/Codes/thornado/SandBox/'
    DataDirectory = Root + 'AdiabaticCollapse_XCFC/Output/'

    #Root = '/lump/data/development/adiabaticCollapse_XCFC/'
    #DataDirectory = Root + 'AdiabaticCollapse_XCFC_nX512_drMin0.50km/'

    iLo = 0
    iHi = 2449

    DD = DensityDecades( DataDirectory, iLo, iHi )
    DD.GetData()
    DD.FindDensityDecades()

    import os
    os.system( 'rm -rf __pycache__' )
