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

## display field in model
#
#
import emerge as em
import numpy as np
from emerge.plot import smith, plot_sp

from emerge.plot import plot_ff, plot_ff_polar  #added for far field plot
import os

simulationObj = em.Simulation("Inverted_F_antenna.FCStd", load_file=True)
simulationResult = simulationObj.data.mw

#######################################################################################################################################
# E FIELD PLOT
#######################################################################################################################################
mm = 0.001
currDir = os.getcwd()

# add model files into display
for geoObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
	simulationObj.display.add_object(geoObj, opacity=0.1)

result = simulationResult.field.find(freq=2450.0*1e6).cutplane(0.001, z=-3.0*mm)
plot_data = result.scalar('Ez','abs')
X, Y, Z, F = plot_data.xyzf
# simulationObj.display.add_surf(X,Y,Z,F)				        #static field display
simulationObj.display.animate().add_surf(X,Y,Z,F, opacity=0.7)	#animated version of display

simulationObj.display.show()

