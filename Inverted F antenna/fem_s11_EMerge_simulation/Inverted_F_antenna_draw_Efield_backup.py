## EMerge simulation - S11
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

result = simulationResult.field.find(freq=2.45e9).cutplane(0.001, z=-3.0*mm)
plot_data = result.scalar('Ez','real')
X, Y, Z, F = plot_data.xyzf
# simulationObj.display.add_surf(X,Y,Z,F)				#static field display
simulationObj.display.animate().add_surf(X,Y,Z,F, opacity=0.7)	#animated version of display

# # another plane perpendicular to antenna to look how it radiates energy that direction
# result = simulationResult.field.find(freq=2.45e9).cutplane(0.001, x=39.0*mm)
# plot_data = result.scalar('Ez','real')
# X, Y, Z, F = plot_data.xyzf
# simulationObj.display.animate().add_surf(X,Y,Z,F, opacity=0.5)	#animated version of display

simulationObj.display.show()
