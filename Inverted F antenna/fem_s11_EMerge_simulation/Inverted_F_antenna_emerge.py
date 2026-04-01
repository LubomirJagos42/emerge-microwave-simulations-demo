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


from emerge.plot import plot_ff, plot_ff_polar  #added for far field plot



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

simulationObj = em.Simulation("Inverted_F_antenna.FCStd", save_file=True)

#######################################################################################################################################
# EXCITATION basic
#######################################################################################################################################
fmin = 2.0*1000000000.0
fmax = 3.0*1000000000.0
resolution = 0.3
npoints = 7
simulationObj.mw.set_frequency_range(fmin, fmax, npoints)
simulationObj.mw.set_resolution(resolution)

#######################################################################################################################################
# MATERIALS AND GEOMETRY
#######################################################################################################################################
materialList = {}

## MATERIAL - FR4
materialList['FR4'] = em.Material(name='FR4', er=4.2, ur=1)
materialList['FR4'].color = '#ffab00'
materialList['FR4'].opacity = 1.0

stepObjectGroup = em.geo.step.STEPItems(name='substrate', filename=os.path.join(currDir,'substrate_gen_model.step'), unit=mm)
for geoObj in stepObjectGroup.objects:
	geoObj.prio_set(9700)
	geoObj.set_material(materialList['FR4'])

## MATERIAL - PEC
materialList['PEC'] = em.lib.PEC
materialList['PEC'].color = '#adb5bd'
materialList['PEC'].opacity = 1.0

stepObjectGroup = em.geo.step.STEPItems(name='top gnd', filename=os.path.join(currDir,'top gnd_gen_model.step'), unit=mm)
for geoObj in stepObjectGroup.objects:
	geoObj.prio_set(9800)
	geoObj.set_material(materialList['PEC'])
materialList['PEC'].color = '#adb5bd'
materialList['PEC'].opacity = 1.0

stepObjectGroup = em.geo.step.STEPItems(name='antenna', filename=os.path.join(currDir,'antenna_gen_model.step'), unit=mm)
for geoObj in stepObjectGroup.objects:
	geoObj.prio_set(9900)
	geoObj.set_material(materialList['PEC'])

## MATERIAL - air
materialList['air'] = em.Material(name='air', er=1, ur=1)


# Imported objects used as boundary conditions
#

position = (40.0, -37.0, 0.0)
position = tuple([x*mm for x in position])
newSphereObj = em.geo.Sphere(radius=80.0*mm, position=position)
newSphereObj.give_name('airbox')
newSphereObj.name = 'airbox'
newSphereObj.prio_set(9600)

#######################################################################################################################################
# PORTS
#######################################################################################################################################
port = {}
portNamesAndNumbersList = {}


## PORT - in - port_in
portStart = [ 39.9836, -10.023, 0 ]
portStop  = [ 41.01, -8.96572, 0 ]
portStart = [k*0.001 for k in portStart]
portStop = [k*0.001 for k in portStop]


port[1] = {}
port[1]['portStart'] = portStart
port[1]['portStop'] = portStop
w = abs(portStart[0] - portStop[0])
h = abs(portStart[1] - portStop[1])
th = abs(portStart[2] - portStop[2])
port[1]['w'] = w
port[1]['h'] = h
port[1]['th'] = th
port[1]['portR'] = 50*1
port[1]['portDirection'] = tuple([0, 1, 0])
port[1]['portExcitationAmplitude'] = 1.0
port[1]['object'] = em.geo.Plate(name='port_1', origin=portStart, u=[w,0,0], v=[0,h,0])
portNamesAndNumbersList["port_in"] = 1

#######################################################################################################################################
# GRID LINES
#######################################################################################################################################

#	max element size for 'antenna'
#
for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
		if geometryObj.name == 'antenna' or geometryObj.name.startswith('antenna_'):
			simulationObj.mesher.set_boundary_size(geometryObj, 0.3 * mm)


#	max element size for 'top gnd'
#
for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
		if geometryObj.name == 'top gnd' or geometryObj.name.startswith('top gnd_'):
			simulationObj.mesher.set_boundary_size(geometryObj, 2.0 * mm)


#	max element size for 'port_in'
#
for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
		if geometryObj.name == 'port_in' or geometryObj.name.startswith('port_in_'):
			simulationObj.mesher.set_size(geometryObj, 0.1 * mm)



#
# First mesh must be created on existing geometry
#
simulationObj.commit_geometry()
simulationObj.generate_mesh()


#
# Now follows boundary condition definition
#
simulationObj.mw.bc.LumpedPort(port[1]['object'], 1, width=port[1]['w'], height=port[1]['h'], direction=port[1]['portDirection'], Z0=port[1]['portR'], power=port[1]['portExcitationAmplitude'])

#######################################################################################################################################
# BOUNDARY CONDITIONS PART
#######################################################################################################################################

# BOUNDARY CONDITION NAME: absorbing
# TYPE: Absorbing
boundary_selection = None
for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
	if geometryObj.name == 'airbox' or geometryObj.name.startswith('airbox'):
		boundary_selection = geometryObj.boundary()

simulationObj.mw.bc.AbsorbingBoundary(boundary_selection)

#######################################################################################################################################
# DISPLAY MODEL
#######################################################################################################################################
simulationObj.view()
simulationObj.view(plot_mesh=True, volume_mesh=False)

#######################################################################################################################################
# RUN and save results
#######################################################################################################################################
simulationResult = simulationObj.mw.run_sweep()

field = simulationResult.field.find(freq=2.45e9)
ff3d = field.farfield_3d(boundary_selection, origin=position)
simulationObj.display.add_field(ff3d.surfplot('normE','abs',True, rmax=40*mm, offset=(position[0], position[1], position[2]+10*mm)))
simulationObj.display.show()


simulationObj.save()

