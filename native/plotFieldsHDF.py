#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import subprocess
plt.style.use( 'Publication.sty' )
plt.rcParams['legend.fontsize'] = 16
plt.rcParams['legend.loc'] = 'upper right'
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 13
plt.rcParams['figure.titlesize'] = 16
plt.rcParams['figure.figsize'] = [12,9]

from ReadFieldsHDF import ReadFieldsHDF

# --- Get user's HOME directory ---
HOME = subprocess.check_output( ["echo $HOME"], shell = True)
HOME = HOME[:-1].decode( "utf-8" ) + '/'

# --- Get user's THORNADO_DIR directory ---
THORNADO_DIR = subprocess.check_output( ["echo $THORNADO_DIR"], shell = True)
THORNADO_DIR = THORNADO_DIR[:-1].decode( "utf-8" ) + '/'

class PlotFieldsHDF:

    def __init__( self, DataDirectory, Snapshots ):

        self.DataDirectory = DataDirectory
        self.Snapshots     = np.array( Snapshots )

        if not self.DataDirectory[-1] == '/': self.DataDirectory += '/'

        self.PathToData = self.DataDirectory + 'AdiabaticCollapse_XCFC'

        self.nFiles = self.Snapshots.shape[0]

        return


    def GetData( self ):

        self.names \
          = ReadFieldsHDF \
              ( self.PathToData, self.Snapshots, \
                CoordinateSystem = 'SPHERICAL', UsePhysicalUnits = True )

        self.r    = self.names['X1'][1]
        self.rC   = self.names['X1_C'][1]
        self.Time = self.names['Time'][1]
        self.nX   = self.rC.shape[0]
        self.nN   = np.int64( self.r.shape[0] / self.rC.shape[0] )

        self.alpha = np.array( [ 1.0 ], np.float64 )

        if self.nN == 2:

          self.WeightsX = np.array( [ 0.5, 0.5 ], np.float64 )

        if self.nFiles > 1:

            self.alpha = np.linspace( 0.2, 1.0, self.nFiles )

        return


    def ComputeCellAverage( self, iSS, Field ):

        SqrtGm = self.names['GF_Sg'][1][iSS,0,0,:]
        uN     = self.names[Field  ][1][iSS,0,0,:]

        uK = np.empty( (self.nX), np.float64 )

        for iX1 in range( self.nX ):

            iLo = self.nN*iX1
            iHi = self.nN*(iX1+1)

            uK[iX1] \
              = np.sum( self.WeightsX * uN[iLo:iHi] * SqrtGm[iLo:iHi] ) \
                  / np.sum( self.WeightsX * SqrtGm[iLo:iHi] )

        return uK


    def AddPlot( self, ax, iSS, Field, c = 'k-', label = '', lw = 2.0, f = '' ):

        ss = 1.0
        if Field == 'PF_V1' or Field == 'GF_b1': ss = 2.99792458e5
        uK = self.ComputeCellAverage( iSS, Field ) / ss

        scale = 1.0
        if not f == '': scale = (2.99792458e10)**2
        if   f == 'lapse': uK = 1.0 + uK / scale
        elif f == 'psi'  : uK = 1.0 - 0.5 * uK / scale

        ax.plot( self.rC, uK, '.', \
                 alpha = self.alpha[iSS], lw = lw, label = str( label ) )

        return

if __name__ == '__main__':

    SaveFig, suffix = False, 'XCFC'

    Snapshots = [ 0, 1 ]

    tb = 2.419e2
    rhoMax = 5.896e14

    PlotVariables = 'Fluid'
    #PlotVariables = 'CFA'
    #PlotVariables = 'Thermo'
    #PlotVariables = 'CFA_FPvXCFC'

    DataDirectory = THORNADO_DIR + 'SandBox/AdiabaticCollapse_XCFC/'
    DataDirectory += 'Output/'

    #DataDirectory = '/lump/data/development/adiabaticCollapse_XCFC/'
    #DataDirectory += 'adiabaticCollapse_XCFC_drMin0.50km_nX512/'

    Plot = PlotFieldsHDF( DataDirectory, Snapshots )
    Plot.GetData()

    FigTitle = 'Adiabatic Collapse (Newtonian)'

    if PlotVariables == 'Fluid':

        Fields = np.array( [ 'PF_D', 'PF_V1', 'AF_P' ], str )

        nRows = 3
        nCols = 1
        fig, axs = plt.subplots( nRows, nCols )
        fig.suptitle( FigTitle )

        for iSS in range( Plot.nFiles ):

            for i in range( Fields.shape[0] ):

                if i == 0:

                    Plot.AddPlot( axs[i], iSS, Field = Fields[i], \
                                  label = r'$t-t_{{b}}={:+.6e}$ ms'.format \
                                    ( Plot.Time[iSS] - tb ) )

                else:

                    Plot.AddPlot( axs[i], iSS, Field = Fields[i] )

        for iF in range( nRows ):

            axs[iF].set_xscale( 'log' )
            axs[iF].set_xlim( Plot.r[0], Plot.r[-1] )
            axs[iF].tick_params( axis = 'both', labelsize = 14 )
            #if iF < nRows-1: axs[iF].xaxis.set_visible( False )
            if iF < nRows-1: axs[iF].xaxis.set_ticklabels([])
            axs[iF].grid()

        axs[0].set_yscale( 'log' )
        axs[2].set_yscale( 'log' )

        axs[0].set_ylabel( r'$\rho\,\left[\mathrm{g\ cm}^{-3}\right]$' )
        axs[1].set_ylabel( r'$v^{1}/c$' )
        axs[2].set_ylabel( r'$p\,\left[\mathrm{erg\ cm}^{-3}\right]$' )

        axs[0].legend( prop = {'size':10} )
        axs[-1].set_xlabel( 'Radial Coordinate [km]' )

        plt.subplots_adjust( hspace = 0.0 )

        if SaveFig:

            plt.savefig( 'fig.AdiabaticCollapse_XCFC_{:}_Fluid.png'.format \
                         ( suffix ), dpi = 300 )

        else:

            plt.show()

        plt.close()

    if PlotVariables == 'CFA':

        Fields = np.array( [ 'GF_al', 'GF_CF', 'GF_b1', 'GF_NP' ], str )

        nRows = 2
        nCols = 1
        fig, axs = plt.subplots( nRows, nCols )
        fig.suptitle( FigTitle )

        for iSS in range( Plot.nFiles ):

            if iSS == Plot.nFiles - 1:

#                Plot.AddPlot( axs[0], iSS, Field = Fields[3], c = 'b--', \
#                              label = r'$\psi_{N}$', lw = 2, f = 'psi' )

                Plot.AddPlot( axs[0], iSS, Field = Fields[1], c = 'k--', \
                              label = r'$\psi$' )

#                Plot.AddPlot( axs[0], iSS, Field = Fields[3], c = 'b-', \
#                              label = r'$\alpha_{N}$', lw = 2, f = 'lapse' )

                Plot.AddPlot( axs[0], iSS, Field = Fields[0], c = 'k-', \
                              label = r'$\alpha$' )

            else:

#                Plot.AddPlot( axs[0], iSS, Field = Fields[3], c = 'b--', \
#                              lw = 2, f = 'psi' )
                Plot.AddPlot( axs[0], iSS, Field = Fields[1], c = 'k--' )
#                Plot.AddPlot( axs[0], iSS, Field = Fields[3], c = 'b-', \
#                              lw = 2, f = 'lapse' )
                Plot.AddPlot( axs[0], iSS, Field = Fields[0], c = 'k-' )

            Plot.AddPlot( axs[1], iSS, Field = Fields[2], \
                          label = r'$t-t_{{b}}={:+.6e}$ ms'.format \
                            ( Plot.Time[iSS] - tb ) )

        for iF in range( nRows ):

            axs[iF].set_xscale( 'log' )
            axs[iF].set_xlim( Plot.r[0], Plot.r[-1] )

        axs[1].set_ylabel( Fields[2] + ' ' + Plot.names[Fields[2]][0] )
        axs[1].set_ylabel( r'$\beta^{1}/c$' )
        #axs[0].xaxis.set_visible( False )
        axs[0].xaxis.set_ticklabels( [] )
        axs[0].grid()
        axs[1].grid()

        axs[0].legend()
        axs[1].legend()
        axs[-1].set_xlabel( 'Radial Coordinate [km]' )

        plt.subplots_adjust( hspace = 0.0 )

        if SaveFig:

            plt.savefig( 'fig.AdiabaticCollapse_XCFC_{:}_XCFC.png'.format \
                         ( suffix ), dpi = 300 )

        else:

            plt.show()

        plt.close()

    if PlotVariables == 'Thermo':

        Fields = np.array( [ 'AF_S', 'AF_T', 'AF_Ye' ], str )

        nRows = Fields.shape[0]
        nCols = 1
        fig, axs = plt.subplots( nRows, nCols )
        fig.suptitle( FigTitle )

        for iF, Field in enumerate( Fields ):

            for iSS in range( Plot.nFiles ):

                Plot.AddPlot( axs[iF], iSS, Field = Field, \
                              label = r'$t-t_{{b}}={:+.6e}$ ms'.format \
                              ( Plot.Time[iSS] - tb ) )

            axs[iF].set_xscale( 'log' )
            axs[iF].set_xlim( Plot.r[0], Plot.r[-1] )

            if iF < Fields.shape[0]-1:
                #axs[iF].xaxis.set_visible( False )
                axs[iF].xaxis.set_ticklabels( [] )
            axs[iF].grid()

        axs[0].set_ylabel( r'$s\,\left[k_{b}/\mathrm{baryon}\right]$' )
        axs[1].set_ylabel( r'$T\,\left[K\right]$' )
        axs[2].set_ylabel( r'$Y_{e}$' )

        axs[1].set_ylim( 5.0e8, 4.0e11 )
        axs[1].legend( prop = {'size':10} )
        axs[-1].set_xlabel( 'Radial Coordinate [km]' )

        #axs[0].set_yscale( 'log' )
        axs[1].set_yscale( 'log' )

        plt.subplots_adjust( hspace = 0.0 )

        if SaveFig:

            plt.savefig( 'fig.AdiabaticCollapse_XCFC_{:}_Thermo.png'.format \
                         ( suffix ), dpi = 300 )

        else:

            plt.show()

        plt.close()

    import os
    os.system( 'rm -rf __pycache__' )
