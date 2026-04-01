## EMerge simulation
#
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
from emerge.plot import smith, plot_sp
#
# Change current path to script file folder
#
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
## constants
unit    = 0.001 # Model coordinates and lengths will be specified in mm.
fc_unit = 0.001 # STL files are exported in FreeCAD standard units (mm).


currDir = os.getcwd()
print(currDir)

## prepare simulation folder, if dir exits remove and create new one to be empty
Sim_Path = os.path.join(currDir, 'simulation_output')
if os.path.exists(Sim_Path):
	shutil.rmtree(Sim_Path)   # clear previous directory
	os.mkdir(Sim_Path)    # create empty simulation folder

# --- Unit definitions -----------------------------------------------------
m = 1.0
cm = 0.01
mm = 0.001  # meters per millimeter
um = 0.000001
nm = 0.000000001

pF = 1e-12  # picofarad in farads
fF = 1e-15  # femtofarad in farads
pH = 1e-12  # picohenry in henrys
nH = 1e-9  # nanohenry in henrys

simulationObj = em.Simulation("FreeCAD EMerge Model")

#######################################################################################################################################
# EXCITATION basic
#######################################################################################################################################
fmin = 0.5*1000000000.0
fmax = 1.0*1000000000.0
resolution = 0.1
npoints = 5
simulationObj.mw.set_frequency_range(fmin, fmax, npoints)
simulationObj.mw.set_resolution(resolution)

#######################################################################################################################################
# MATERIALS AND GEOMETRY
#######################################################################################################################################
materialList = {}

## MATERIAL - PEC
materialList['PEC'] = em.lib.PEC
materialList['PEC'].color = '#acb5bc'
materialList['PEC'].opacity = 1.0

stepObjectGroup = em.geo.step.STEPItems(name='Face', filename=os.path.join(currDir,'Face_gen_model.step'), unit=mm)
for geoObj in stepObjectGroup.objects:
	geoObj.prio_set(10000)
	geoObj.set_material(materialList['PEC'])
materialList['PEC'].color = '#acb5bc'
materialList['PEC'].opacity = 1.0

stepObjectGroup = em.geo.step.STEPItems(name='Face001', filename=os.path.join(currDir,'Face001_gen_model.step'), unit=mm)
for geoObj in stepObjectGroup.objects:
	geoObj.prio_set(10000)
	geoObj.set_material(materialList['PEC'])

em.geo.Sphere(190*mm, (54*mm, -54*mm, 0))

#######################################################################################################################################
# GRID LINES
#######################################################################################################################################

#	max element size for 'Face'
#
for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
		if geometryObj.name == 'Face' or geometryObj.name.startswith('Face_'):
			simulationObj.mesher.set_boundary_size(geometryObj, 1.0 * mm)
			# simulationObj.mesher.set_face_size(geometryObj, 1.0 * mm)


#	max element size for 'Face001'
#
for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
		if geometryObj.name == 'Face001' or geometryObj.name.startswith('Face001_'):
			simulationObj.mesher.set_boundary_size(geometryObj, 1.0 * mm)
			# simulationObj.mesher.set_face_size(geometryObj, 1.0 * mm)



#
# First mesh must be created on existing geometry
#
simulationObj.commit_geometry()
simulationObj.generate_mesh()


#
# Now follows boundary condition definition
#

#######################################################################################################################################
# DISPLAY MODEL
#######################################################################################################################################
simulationObj.view()
simulationObj.view(plot_mesh=True, volume_mesh=False)

#######################################################################################################################################
# RUN
#######################################################################################################################################
simulationResult = simulationObj.mw.run_sweep()

freqs = simulationResult.scalar.grid.freq
freq_dense = np.linspace(fmin, fmax, 1001)
S11 = simulationResult.scalar.grid.model_S(1, 1, freq_dense)  # reflection coefficient
plot_sp(freq_dense, S11)  # plot return loss in dB
smith(S11, f=freq_dense, labels='S11')  # Smith chart of S11

