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

simulationObj = em.Simulation("Patch_Antenna_Simple", save_file=True)

#######################################################################################################################################
# EXCITATION basic
#######################################################################################################################################
fmin = 1.0*1000000000.0
fmax = 2.0*1000000000.0
resolution = 0.2
npoints = 7
simulationObj.mw.set_frequency_range(fmin, fmax, npoints)
simulationObj.mw.set_resolution(resolution)

#######################################################################################################################################
# MATERIALS AND GEOMETRY
#######################################################################################################################################
materialList = {}

## MATERIAL - FR4
materialList['FR4'] = em.Material(name='FR4', er=4.2, ur=1.0, tand=0.0, cond=0.0)
materialList['FR4'].color = '#ffab00'
materialList['FR4'].opacity = -89.0

stepObjectGroup = em.geo.step.STEPItems(name='substrate', filename=os.path.join(currDir,'substrate_gen_model.step'), unit=mm)
for geoObj in stepObjectGroup.objects:
	geoObj.prio_set(9700)
	geoObj.set_material(materialList['FR4'])

## MATERIAL - PEC
materialList['PEC'] = em.lib.PEC
materialList['PEC'].color = '#00ffff'
materialList['PEC'].opacity = -89.0

stepObjectGroup = em.geo.step.STEPItems(name='patch', filename=os.path.join(currDir,'patch_gen_model.step'), unit=mm)
for geoObj in stepObjectGroup.objects:
	geoObj.prio_set(9900)
	geoObj.set_material(materialList['PEC'])
materialList['PEC'].color = '#acb5bc'
materialList['PEC'].opacity = 1.0

stepObjectGroup = em.geo.step.STEPItems(name='gnd', filename=os.path.join(currDir,'gnd_gen_model.step'), unit=mm)
for geoObj in stepObjectGroup.objects:
	geoObj.prio_set(9800)
	geoObj.set_material(materialList['PEC'])


# Imported objects used as boundary conditions
#

position = (0.0, 0.0, 0.0)
position = tuple([x*mm for x in position])
newSphereObj = em.geo.Sphere(radius=140.0*mm, position=position)
newSphereObj.give_name('airbox')
newSphereObj.name = 'airbox'
newSphereObj.prio_set(9600)

#######################################################################################################################################
# PORTS
#######################################################################################################################################
port = {}
portNamesAndNumbersList = {}


## PORT - in - port in
portStart = [ -1.21636, -38.3474, -1.5 ]
portStop  = [ 1.1308, -38.3474, 0 ]
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
port[1]['portR'] = 50.0*1
port[1]['portDirection'] = em.ZAX
port[1]['portExcitationAmplitude'] = 1.0
port[1]['object'] = em.geo.Plate(name='port in', origin=portStart, u=[w,0,0], v=[0,0,th])
portNamesAndNumbersList["port in"] = 1

#######################################################################################################################################
# GRID LINES
#######################################################################################################################################

#	max element size for 'gnd'
#
for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
		if geometryObj.name == 'gnd' or geometryObj.name.startswith('gnd_'):
			simulationObj.mesher.set_face_size(geometryObj, 5.5 * mm)


#	max element size for 'substrate'
#
for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
		if geometryObj.name == 'substrate' or geometryObj.name.startswith('substrate_'):
			simulationObj.mesher.set_domain_size(geometryObj, 1.5 * mm)


#	max element size for 'patch'
#
for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
		if geometryObj.name == 'patch' or geometryObj.name.startswith('patch_'):
			simulationObj.mesher.set_face_size(geometryObj, 4.5 * mm)
			simulationObj.mesher.set_boundary_size(geometryObj, 1.5 * mm)



#
# First mesh must be created on existing geometry
#
simulationObj.commit_geometry()
simulationObj.generate_mesh()


#
# Now follows boundary condition definition
#
simulationObj.mw.bc.LumpedPort(port[1]['object'], 1, width=port[1]['w'], height=port[1]['th'], direction=port[1]['portDirection'], Z0=port[1]['portR'], power=port[1]['portExcitationAmplitude'])

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

createGmshNamedGroup('substrate', 'substrate')
createGmshNamedGroup('gnd', 'gnd')
createGmshNamedGroup('patch', 'patch')
createGmshNamedGroup('port in', 'port in')
createGmshNamedGroup('airbox', 'airboxBoundary', useBoundary=True)

simulationObj.export('Patch_Antenna_Simple.msh')

#######################################################################################################################################
# DISPLAY MODEL
#######################################################################################################################################
simulationObj.view()
simulationObj.view(plot_mesh=True, volume_mesh=False)

#######################################################################################################################################
# RUN and save results
#######################################################################################################################################
simulationResult = simulationObj.mw.run_sweep()
simulationObj.save()

