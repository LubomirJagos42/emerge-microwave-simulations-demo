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
import gmsh

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

simulationObj = em.Simulation("Wilkinson Divider", save_file=True)

#######################################################################################################################################
# EXCITATION basic
#######################################################################################################################################
fmin = 0.5*1000000000.0
fmax = 5.0*1000000000.0
resolution = 0.2
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
	geoObj.prio_set(9400)
	geoObj.set_material(materialList['FR4'])

## MATERIAL - PEC
materialList['PEC'] = em.lib.PEC
materialList['PEC'].color = '#0054ff'
materialList['PEC'].opacity = 1.0

stepObjectGroup = em.geo.step.STEPItems(name='wilkinson whole trace', filename=os.path.join(currDir,'wilkinson whole trace_gen_model.step'), unit=mm)
for geoObj in stepObjectGroup.objects:
	geoObj.prio_set(9600)
	geoObj.set_material(materialList['PEC'])
materialList['PEC'].color = '#0054ff'
materialList['PEC'].opacity = 1.0

stepObjectGroup = em.geo.step.STEPItems(name='gnd', filename=os.path.join(currDir,'gnd_gen_model.step'), unit=mm)
for geoObj in stepObjectGroup.objects:
	geoObj.prio_set(9500)
	geoObj.set_material(materialList['PEC'])

## MATERIAL - air
materialList['air'] = em.Material(name='air', er=1, ur=1)
materialList['air'].color = '#abffff'
materialList['air'].opacity = -79.0

stepObjectGroup = em.geo.step.STEPItems(name='simbox', filename=os.path.join(currDir,'simbox_gen_model.step'), unit=mm)
for geoObj in stepObjectGroup.objects:
	geoObj.prio_set(9300)
	geoObj.set_material(materialList['air'])


# Imported objects used as boundary conditions
#

stepObjectGroup = em.geo.step.STEPItems(name='simbox', filename=os.path.join(currDir,'simbox_gen_model.step'), unit=mm)
for geoObj in stepObjectGroup.objects:
	geoObj.prio_set(10000)

#######################################################################################################################################
# PORTS
#######################################################################################################################################
port = {}
portNamesAndNumbersList = {}


## PORT - in - port in
portStart = [ -1.22377, 16.3356, -1.5 ]
portStop  = [ 1.19803, 16.3356, 0 ]
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
port[1]['object'] = em.geo.Plate(name='port in', origin=portStart, u=[w,0,0], v=[0,0,th])
portNamesAndNumbersList["port in"] = 1

## PORT - out - port out 1
portStart = [ -19.2144, -15.3642, -1.5 ]
portStop  = [ -19.2144, -13.229, 0 ]
portStart = [k*0.001 for k in portStart]
portStop = [k*0.001 for k in portStop]


port[2] = {}
port[2]['portStart'] = portStart
port[2]['portStop'] = portStop
w = abs(portStart[0] - portStop[0])
h = abs(portStart[1] - portStop[1])
th = abs(portStart[2] - portStop[2])
port[2]['w'] = w
port[2]['h'] = h
port[2]['th'] = th
port[2]['portR'] = 50*1
port[2]['portDirection'] = em.ZAX
port[2]['portExcitationAmplitude'] = 1.0
port[2]['object'] = em.geo.Plate(name='port out 1', origin=portStart, u=[0,h,0], v=[0,0,th])
portNamesAndNumbersList["port out 1"] = 2
## PORT - out - port out 2
portStart = [ 19.049, -15.3376, -1.5 ]
portStop  = [ 19.049, -13.1621, 0 ]
portStart = [k*0.001 for k in portStart]
portStop = [k*0.001 for k in portStop]


port[3] = {}
port[3]['portStart'] = portStart
port[3]['portStop'] = portStop
w = abs(portStart[0] - portStop[0])
h = abs(portStart[1] - portStop[1])
th = abs(portStart[2] - portStop[2])
port[3]['w'] = w
port[3]['h'] = h
port[3]['th'] = th
port[3]['portR'] = 50*1
port[3]['portDirection'] = em.ZAX
port[3]['portExcitationAmplitude'] = 1.0
port[3]['object'] = em.geo.Plate(name='port out 2', origin=portStart, u=[0,h,0], v=[0,0,th])
portNamesAndNumbersList["port out 2"] = 3

#######################################################################################################################################
# GRID LINES
#######################################################################################################################################

#	max element size for 'wilkinson whole trace'
#
for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
		if geometryObj.name == 'wilkinson whole trace' or geometryObj.name.startswith('wilkinson whole trace_'):
			simulationObj.mesher.set_boundary_size(geometryObj, 0.3 * mm)
			simulationObj.mesher.set_face_size(geometryObj, 0.3 * mm)


#	max element size for 'gnd'
#
for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
		if geometryObj.name == 'gnd' or geometryObj.name.startswith('gnd_'):
			simulationObj.mesher.set_face_size(geometryObj, 3.0 * mm)


#	max element size for 'substrate'
#
for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
		if geometryObj.name == 'substrate' or geometryObj.name.startswith('substrate_'):
			simulationObj.mesher.set_domain_size(geometryObj, 0.5 * mm)



#
# First mesh must be created on existing geometry
#
simulationObj.commit_geometry()

gmsh.model.occ.removeAllDuplicates()
gmsh.model.occ.synchronize()


def createGmshNamedGroup(geometryObjName: str, groupName: str, groupTag: int = -1, useBoundary: bool = False, useSuffixToRecognizeGeometryName: bool = True):
	objectTag1DList = []
	objectTag2DList = []
	objectTag3DList = []
	seen_tags = set()

	for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
		if geometryObj.name == geometryObjName or geometryObj.name.startswith(geometryObjName + ('_' if useSuffixToRecognizeGeometryName else '')):
			for tagTuple in (geometryObj.boundary().dimtags if useBoundary else geometryObj.dimtags):
				tag = tagTuple[1]
				if tag not in seen_tags:
					seen_tags.add(tag)
					if tagTuple[0] == 1:
						objectTag1DList.append(tagTuple[1])
					if tagTuple[0] == 2:
						objectTag2DList.append(tagTuple[1])
					if tagTuple[0] == 3:
						objectTag3DList.append(tagTuple[1])
				else:
					print(f"WARNING: Duplicate tag {tag} found!")


	if groupTag > -1:
		gmsh.model.addPhysicalGroup(1, objectTag1DList, name=groupName, tag=groupTag)
		gmsh.model.addPhysicalGroup(2, objectTag2DList, name=groupName, tag=groupTag + 1)
		gmsh.model.addPhysicalGroup(3, objectTag3DList, name=groupName, tag=groupTag + 2)
	else:
		gmsh.model.addPhysicalGroup(1, objectTag1DList, name=groupName)
		gmsh.model.addPhysicalGroup(2, objectTag2DList, name=groupName)
		gmsh.model.addPhysicalGroup(3, objectTag3DList, name=groupName)

createGmshNamedGroup('simbox', 'simbox', 1000)
createGmshNamedGroup('port in', 'port in', 2000)
createGmshNamedGroup('port out 2', 'port out 2', 3000)
createGmshNamedGroup('gnd', 'gnd', 4000)
createGmshNamedGroup('substrate', 'substrate', 5000)
createGmshNamedGroup('wilkinson whole trace', 'wilkinson whole trace', 6000)
createGmshNamedGroup('port out 1', 'port out 1', 7000)
createGmshNamedGroup('simbox', 'simboxBoundary', 8000, useBoundary=True)












simulationObj.generate_mesh()


#
# Now follows boundary condition definition
#
simulationObj.mw.bc.LumpedPort(port[1]['object'], 1, width=port[1]['w'], height=port[1]['th'], direction=port[1]['portDirection'], Z0=port[1]['portR'], power=port[1]['portExcitationAmplitude'])
simulationObj.mw.bc.LumpedPort(port[2]['object'], 2, width=port[2]['h'], height=port[2]['th'], direction=port[2]['portDirection'], Z0=port[2]['portR'])
simulationObj.mw.bc.LumpedPort(port[3]['object'], 3, width=port[3]['h'], height=port[3]['th'], direction=port[3]['portDirection'], Z0=port[3]['portR'])



gmsh.model.mesh.removeDuplicateNodes()
gmsh.model.mesh.removeDuplicateElements()






#######################################################################################################################################
# BOUNDARY CONDITIONS PART
#######################################################################################################################################

# BOUNDARY CONDITION NAME: absorbing
# TYPE: Absorbing
boundary_selection = None
for geometryObj in simulationObj.state.manager.geometry_list[simulationObj.modelname].values():
	if geometryObj.name == 'simbox' or geometryObj.name.startswith('simbox'):
		boundary_selection = geometryObj.boundary()

simulationObj.mw.bc.AbsorbingBoundary(boundary_selection)

#######################################################################################################################################
# EXPERIMENT EXPORT MESH WITH NAMED GROUP OF MESH
#######################################################################################################################################
simulationObj.export('Wilkinson Divider.msh')
simulationObj.export('Wilkinson Divider.med')

#######################################################################################################################################
# DISPLAY MODEL
#######################################################################################################################################
simulationObj.view()
simulationObj.view(plot_mesh=True, volume_mesh=False)

#######################################################################################################################################
# RUN and save results
#######################################################################################################################################
#simulationResult = simulationObj.mw.run_sweep()
#simulationObj.save()

