## EMerge simulation - S11
#
#
import emerge as em
import numpy as np
from emerge.plot import smith, plot_sp
import os

simulationObj = em.Simulation("Discone Antenna.FCStd", load_file=True)
simulationResult = simulationObj.data.mw

#######################################################################################################################################
# EXCITATION basic
#######################################################################################################################################
fmin = 0.5*1000000000.0
fmax = 5.0*1000000000.0
resolution = 0.3
npoints = 7
simulationObj.mw.set_frequency_range(fmin, fmax, npoints)
simulationObj.mw.set_resolution(resolution)

freqs = simulationResult.scalar.grid.freq
freq_dense = np.linspace(fmin, fmax, 101)

# S11 = simulationResult.scalar.grid.model_S(1, 1, freq_dense)  # reflection coefficient
# plot_sp(freq_dense, S11)  # plot return loss in dB
# smith(S11, f=freq_dense, labels='S11')  # Smith chart of S11

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
# field = simulationResult.field.find(freq=1.6e9)
field = simulationResult.field.find(freq=2.5e9)
ff3d = field.farfield_3d(boundary_selection, origin=(0.0, 0.0, 0.0))
# simulationObj.display.add_field(ff3d.surfplot('normE','abs',True, dB=True, rmax=150*mm, offset=(0.0, 0.0, 70.0*mm)))
simulationObj.display.add_field(ff3d.surfplot('normE','abs',True, dB=True, rmax=150*mm, offset=(0.0, 0.0, -2*70.0*mm)))
simulationObj.display.show()
