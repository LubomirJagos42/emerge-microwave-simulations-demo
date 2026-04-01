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

simulationObj = em.Simulation("Inverted_F_antenna.FCStd", load_file=True)
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
field = simulationResult.field.find(freq=2450.0*1e6)
ff3d = field.farfield_3d(boundary_selection, origin=(0.0*mm, 0.0*mm, 0.0*mm))
# simulationObj.display.add_field(ff3d.surfplot('normE','abs',True, dB=True, rmax=40.0*mm, offset=(0.0, 0.0, 0.0)))

fieldEObj = ff3d.surfplot('normE','abs',True, dB=True, rmax=40.0*mm, offset=(0.0, 0.0, 0.0))
simulationObj.display.add_field(fieldEObj)

#######################################################################################################
#	EXTRACT ALL OBJECTS FROM PYVISTA SCENE - using internal methods as there is no public api for this
#######################################################################################################

import pyvista as pv
plotter = simulationObj.display._plot
# Print everything in the plotter to find the farfield mesh
print(f"Number of actors: {len(plotter.actors)}")
for name, actor in plotter.actors.items():
    print(f"  name: {name}")
    mapper = actor.GetMapper()
    if mapper and mapper.GetInput():
        mesh = pv.wrap(mapper.GetInput())
        print(f"    points={mesh.n_points}  cells={mesh.n_cells}  arrays={mesh.array_names}")

index = 1
renderer = plotter.renderer
for actor in renderer.GetActors():
    mapper = actor.GetMapper()
    if mapper:
        data = mapper.GetInput()
        if data:
            mesh = pv.wrap(data)
            print(f"Points: {mesh.n_points}  Cells: {mesh.n_cells}  Arrays: {mesh.array_names}")
            if mesh.n_points > 0:
                mesh.save(f"farfield_from_scene_{index}.vtk")
                index += 1
                print("✓ Saved")

simulationObj.display.show()

