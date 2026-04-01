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

simulationObj = em.Simulation("Helical_Antenna", save_file=True)

#######################################################################################################################################
# EXCITATION 2.4GHz
#######################################################################################################################################
fmin = 1.3*1000000000.0
fmax = 3.0*1000000000.0
resolution = 0.33
npoints = 11
simulationObj.mw.set_frequency_range(fmin, fmax, npoints)
simulationObj.mw.set_resolution(resolution)

#######################################################################################################################################
# MATERIALS AND GEOMETRY
#######################################################################################################################################
materialList = {}

## MATERIAL - PEC
materialList['PEC'] = em.lib.PEC

## MATERIAL - air
materialList['air'] = em.Material(name='air', er=1, ur=1)
materialList['air'].color = '#abffff'
materialList['air'].opacity = -89.0

position = (0.0, 0.0, 81.5)
position = tuple([x*mm for x in position])
newSphereObj = em.geo.Sphere(radius=350.0*mm, position=position)
newSphereObj.give_name('airbox')
newSphereObj.name = 'airbox'
newSphereObj.prio_set(9600)


# Imported objects used as boundary conditions
#
antennaSpiralObject = None
stepObjectGroup = em.geo.step.STEPItems(name='helical_antenna_spiral', filename=os.path.join(currDir,'helical_antenna_spiral_gen_model.step'), unit=mm)
for geoObj in stepObjectGroup.objects:
	geoObj.prio_set(9900)
	antennaSpiralObject = geoObj

stepObjectGroup = em.geo.step.STEPItems(name='gnd face', filename=os.path.join(currDir,'gnd face_gen_model.step'), unit=mm)
for geoObj in stepObjectGroup.objects:
	geoObj.prio_set(10000)

position = (0.0, 0.0, 81.5)
position = tuple([x*mm for x in position])
newSphereObj = em.geo.Sphere(radius=350.0*mm, position=position)
newSphereObj.give_name('airbox')
newSphereObj.name = 'airbox'
newSphereObj.prio_set(9700)

#######################################################################################################################################
# PORTS
#######################################################################################################################################
port = {}
portNamesAndNumbersList = {}


## PORT - input - feed_port
portStart = [ 13.7721, 1, 0.35 ]
portStop  = [ 18.1175, 1, 4.76936 ]
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
port[1]['portDirection'] = em.ZAX
port[1]['portExcitationAmplitude'] = 1.0

#
# IMPORTANT: Need to cut spiral from port to have not overlapping facet and 3D spiral object!!!
#
portGeometryObject = em.geo.Plate(name='feed_port', origin=portStart, u=[w,0,0], v=[0,0,th])
portGeometryObject = em.geo.remove(portGeometryObject, antennaSpiralObject, remove_tool=False)
port[1]['object'] = em.geo.Plate(name='feed_port', origin=portStart, u=[w,0,0], v=[0,0,th])

portNamesAndNumbersList["feed_port"] = 1

#######################################################################################################################################
# GRID LINES
#######################################################################################################################################
simulationObj.commit_geometry()

#	max element size for 'airbox'
#
for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
		if geometryObj.name == 'airbox' or geometryObj.name.startswith('airbox_'):
			simulationObj.mesher.set_size(geometryObj, 50.0 * mm)


#	max element size for 'feed_port'
#
for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
		if geometryObj.name == 'feed_port' or geometryObj.name.startswith('feed_port_'):
			simulationObj.mesher.set_size(geometryObj, 1.0 * mm)


#	max element size for 'helical_antenna_spiral'
#
for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
		if geometryObj.name == 'helical_antenna_spiral' or geometryObj.name.startswith('helical_antenna_spiral_'):
			simulationObj.mesher.set_size(geometryObj, 5.0 * mm)


#	max element size for 'gnd face'
#
for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
		if geometryObj.name == 'gnd face' or geometryObj.name.startswith('gnd face_'):
			simulationObj.mesher.set_size(geometryObj, 10.0 * mm)



#
# First mesh must be created on existing geometry
#
# simulationObj.commit_geometry()

#display model
# simulationObj.view()

simulationObj.generate_mesh()


#
# Now follows boundary condition definition
#
simulationObj.mw.bc.LumpedPort(port[1]['object'], 1, width=port[1]['w'], height=port[1]['th'], direction=port[1]['portDirection'], Z0=port[1]['portR'], power=port[1]['portExcitationAmplitude'])

#######################################################################################################################################
# BOUNDARY CONDITIONS PART
#######################################################################################################################################

# BOUNDARY CONDITION NAME: PEC
# TYPE: PEC
boundary_selection = None
for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
	if geometryObj.name == 'helical_antenna_spiral' or geometryObj.name.startswith('helical_antenna_spiral'):
		boundary_selection = geometryObj.boundary()

simulationObj.mw.bc.PEC(boundary_selection)
# simulationObj.mw.bc.PECBoundary(boundary_selection)
boundary_selection = None
for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
	if geometryObj.name == 'gnd face' or geometryObj.name.startswith('gnd face'):
		# boundary_selection = geometryObj.boundary()
		boundary_selection = geometryObj

# simulationObj.mw.bc.PECBoundary(boundary_selection)
simulationObj.mw.bc.PEC(boundary_selection)


# BOUNDARY CONDITION NAME: absorbing
# TYPE: Absorbing
boundary_selection = None
for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
	if geometryObj.name == 'airbox' or geometryObj.name.startswith('airbox'):
		boundary_selection = geometryObj.boundary()

simulationObj.mw.bc.AbsorbingBoundary(boundary_selection)

#######################################################################################################################################
# EXPERIMENT EXPORT MESH WITH NAMED GROUP OF MESH
#######################################################################################################################################
import gmsh

def createGmshNamedGroup(geometryObjName: str, groupName: str, groupTag: int = -1, useBoundary: bool = False, useSuffixToRecognizeGeometryName: bool = True):
	objectTag1DList = []
	objectTag2DList = []
	objectTag3DList = []

	for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
		if geometryObj.name == geometryObjName or geometryObj.name.startswith(geometryObjName + ('_' if useSuffixToRecognizeGeometryName else '')):
			for tagTuple in (geometryObj.boundary().dimtags if useBoundary else geometryObj.dimtags):
				if tagTuple[0] == 1:
					objectTag1DList.append(tagTuple[1])
				if tagTuple[0] == 2:
					objectTag2DList.append(tagTuple[1])
				if tagTuple[0] == 3:
					objectTag3DList.append(tagTuple[1])

	if groupTag > -1:
		gmsh.model.addPhysicalGroup(1, objectTag1DList, name=groupName, tag=groupTag)
		gmsh.model.addPhysicalGroup(2, objectTag2DList, name=groupName, tag=groupTag + 1)
		gmsh.model.addPhysicalGroup(3, objectTag3DList, name=groupName, tag=groupTag + 2)
	else:
		gmsh.model.addPhysicalGroup(1, objectTag1DList, name=groupName)
		gmsh.model.addPhysicalGroup(2, objectTag2DList, name=groupName)
		gmsh.model.addPhysicalGroup(3, objectTag3DList, name=groupName)

createGmshNamedGroup('airbox', 'airbox')
createGmshNamedGroup('feed_port', 'feed_port')
createGmshNamedGroup('helical_antenna_spiral', 'helical_antenna_spiralBoundary', useBoundary=True)
createGmshNamedGroup('airbox', 'airboxBoundary', useBoundary=True)
createGmshNamedGroup('gnd face', 'gnd faceBoundary', useBoundary=False)

simulationObj.export('Helical_Antenna.msh')

#######################################################################################################################################
# DISPLAY MODEL
#######################################################################################################################################
simulationObj.view()
simulationObj.view(plot_mesh=True, volume_mesh=False)

#######################################################################################################################################
# RUN and save results
#######################################################################################################################################
simulationObj.settings.check_ram=False

simulationResult = simulationObj.mw.run_sweep()
simulationObj.save()

