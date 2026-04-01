# Plot far field for structure.
#
# To be run with python.
# FreeCAD to OpenEMS plugin but this time it generates EMerge by Lubomir Jagos, 
# see https://github.com/LubomirJagos42/FreeCAD-OpenEMS-Export
#
# This file has been automatically generated. Manual changes may be overwritten.
#

### Import Libraries
import math
import numpy as np
import emerge as em
import os, tempfile, shutil

# Change current path to script file folder
#
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
## constants
unit    = 0.001 # Model coordinates and lengths will be specified in mm.
fc_unit = 0.001 # STL files are exported in FreeCAD standard units (mm).

currDir = os.getcwd()
Sim_Path = os.path.join(currDir, r'simulation_output')
print(currDir)


#######################################################################################################################################
# Farfield plot and 3D gain generated
#######################################################################################################################################
import emerge as em
import numpy as np
from emerge.plot import smith, plot_sp
import os

simulationObj = em.Simulation("Helical_Antenna", load_file=True)
simulationResult = simulationObj.data.mw

#######################################################################################################################################
# FAR FIELD PLOT
#######################################################################################################################################
mm = 0.001
currDir = os.getcwd()

#######################################################################################################################################
#   ADD BOUNDARY SELECTION SAME AS SIMULATION FILE
#######################################################################################################################################

boundary_selection = None
for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
	if geometryObj.name == 'airbox' or geometryObj.name.startswith('airbox'):
		boundary_selection = geometryObj.boundary()

simulationObj.mw.bc.AbsorbingBoundary(boundary_selection)


# add model files into display
for geoObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
	simulationObj.display.add_object(geoObj)

# display far field
field = simulationResult.field.find(freq=1980.0*1e6)
ff3d = field.farfield_3d(boundary_selection, origin=(0.0*mm, 0.0*mm, 0.0*mm))
# simulationObj.display.add_field(ff3d.surfplot('normE','abs',True, dB=True, rmax=80.0*mm, offset=(0.0, 0.0, 260.0*mm)))
# simulationObj.display.show()

#########################################################################################################################################
#	EXTRACT Efield and compute directivity diagram
#########################################################################################################################################
import pandas as pd
import numpy as np

outputFile = "farfield_results.csv"

n = len(ff3d.theta.flatten())
df = pd.DataFrame({
    'f (GHz)':   np.full(n, ff3d.freq/1e9),
    'theta (deg.)':   np.rad2deg(ff3d.theta.flatten()),
    'phi (deg.)':     np.rad2deg(ff3d.phi.flatten()),
    'r*Re{E_x} (V)':   np.real(ff3d.Ex.flatten()),
    'r*Im{E_x} (V)':   np.imag(ff3d.Ex.flatten()),
    'r*Re{E_y} (V)':   np.real(ff3d.Ey.flatten()),
    'r*Im{E_y} (V)':   np.imag(ff3d.Ey.flatten()),
    'r*Re{E_z} (V)':   np.real(ff3d.Ez.flatten()),
    'r*Im{E_z} (V)':   np.imag(ff3d.Ez.flatten())
})

# Add any other arrays you have
# df['Ex_re'] = ff3d.Ex_re
# df['Ex_im'] = ff3d.Ex_im

df.to_csv(outputFile, index=False)
print(f"✓ Saved {len(df)} rows to {outputFile}")

###############################################################################################################
#   SAVE GAIN AND DIRECTIVITY TO CSV FILE
###############################################################################################################
outputFile = "farfield_gain_directivity_results.csv"

n = len(ff3d.theta.flatten())
df = pd.DataFrame({
    'f (GHz)':   np.full(n, ff3d.freq/1e9),
    'theta (deg.)':   np.rad2deg(ff3d.theta.flatten()),
    'phi (deg.)':     np.rad2deg(ff3d.phi.flatten()),
    'gain (dBi)':   ff3d.gain.norm.flatten(),
    'directivity (dBi)':   ff3d.dir.norm.flatten(),
})

df.to_csv(outputFile, index=False)
print(f"✓ Saved {len(df)} rows to {outputFile}")

###############################################################################################################
#   PLOT 3D DIAGRAMS
###############################################################################################################

from MfemMesherPackage import PlotDiagramUtils

plotter = PlotDiagramUtils()
plotter.readFromFileAndPlotFarfield("farfield_results.csv", outputFile="farfield_3d_Efield.vtk", useDecibels=True, useNormalization=False)
plotter.readFromFileComputeDirectivityRadiationDiagram("farfield_results.csv", outputfile="farfield_3d_directivity.vtk")





