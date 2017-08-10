# -*- coding: utf-8 -*-
"""
Created on Mon July 24 10:09:46 2017
@author: Zoltan Cseresnyes
@affiliation: Research Group Applied Systems Biology, Leibniz Institute for 
Natural Product Research and Infection Biology – Hans Knöll Institute (HKI),
Beutenbergstrasse 11a, 07745 Jena, Germany.
@email: zoltan.cseresnyes@leibniz-hki.de or zcseresn@gmail.com
This is a Python script for performing automated rotations and consecutive rendering of VRML surfaces. 
Full details can be found in our paper Kriegel et al., Cytometry A 2017-2018. If any part 
of the code is used for academic purposes or publications, please cite the 
above mentioned paper.
Copyright (c) 2016-2017, 
Leibniz Institute for Natural Product Research and Infection Biology – 
Hans Knöll Institute (HKI)
Licence: BSD-3-Clause, see ./LICENSE or 
https://opensource.org/licenses/BSD-3-Clause for full details
"""

# v.0.9 reads in all .wrl files from the source folder, i.e. no need for special names, 2.8.17
# v.0.10 add the option to set the color of the surface, also changes the output name rule to reflect original name; 3.8.2017
# v.0.11 fixes the rotation number error and adds copyright header; 3.8.17
# v.1.0 First release version, based on v.0.11; 10.8.17

import bpy
from bpy import context
import bmesh
import math
from mathutils import Vector
from math import sqrt
import mathutils
import random
import os
import numpy as np
import csv
import time

"""Users' data and other settings: """
fileFormat = 'TIFF'
changeObjectColor = True
newObjectColor = (0.0, 0.2, 0.0) #RGB 0.0-1.0, sum=1.0, use 0.1 each for dark grey
turnOffLamps = False
addSecondLamp = False #2nd lamp positioned next to the camera so that each scene is illuminated
rotationSize = np.pi
numberOfRotations = 6
seededRandom = True
deleteAllAtEnd = False
deleteCellPerCycle = True
sleepTime = 0.0
refreshScene = True
printMessages = True
camera_location= (30.0, 65.0, 65.0)
output_filenameTag = "_rendered"
"""End of users' input"""

def look_at(obj_camera, point):
    loc_camera = obj_camera.matrix_world.to_translation()
    direction = point - loc_camera
    # point the cameras '-Z' and use its 'Y' as up
    rot_quat = direction.to_track_quat('-Z', 'Y')
    # assume we're using euler rotation
    obj_camera.rotation_euler = rot_quat.to_euler()
    
file = os.path.splitext(bpy.data.filepath)[0]
print("Blender file running: ", file)
print(" Starting 3D object rotation and rendering ")
print(time.strftime("%d/%m/%Y"))
print("Current time " , time.strftime("%X"))
 
"""Put the full path to the data folder here:"""
path = "/home/zoltan/Schreibtisch/Daten_sync/Collaborations/ShapeAnalysis_Fabi_Ralf/Simons_data/newAnalysisForPaper_2017/Surfaces/RestingCells"

#Add a new lamp:
if addSecondLamp == True:
    bpy.ops.object.lamp_add(type='SUN', radius=1, view_align=False, location=camera_location, 
    layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.context.object.data.shadow_soft_size = 0.01
    bpy.context.object.data.cycles.cast_shadow = True

if turnOffLamps == True:
    output_filenameTag += "_noLight"
    bpy.data.objects["Lamp"].data.energy = 0
    if addSecondLamp == True:
        bpy.data.objects["Sun"].data.energy = 0



print()
print("***************************")
print()
print("Data folder:", path)

"""Get the list of all files in directory:"""
file_list = os.listdir(path)

"""Here is the list of file name endings that indetify .wrl files of the various components: 
    cortex filename ends with 447
    sinusoids filename ends with 593
    arterioles filename ends with 655
    PCs filename ends with 525
    shoebox filename ends with Shoebox"""
obj_list_plasmaCells = [item for item in file_list if item[-3:] == 'wrl']

print()
print("# of files for PC: ", len(obj_list_plasmaCells))

plasmaCells = [] 

#Set the rendering parameters
bpy.context.scene.render.resolution_x = 1360
bpy.context.scene.render.resolution_y = 1024
bpy.context.scene.render.resolution_percentage = 50
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = len(obj_list_plasmaCells)
bpy.context.scene.frame_step = 1
bpy.context.scene.render.pixel_aspect_x = 1
bpy.context.scene.render.pixel_aspect_y = 1
bpy.context.scene.render.use_file_extension = True
bpy.context.scene.render.image_settings.color_mode ='RGBA'
bpy.context.scene.render.image_settings.file_format=fileFormat 
bpy.context.scene.render.image_settings.compression = 90

plasmaCells = []
""" Open PCs from .wrl files one by one and rotate them randomly"""
for pc in obj_list_plasmaCells:
    full_path_to_pc = os.path.join(path, pc)
    bpy.ops.import_scene.x3d(filepath=full_path_to_pc)
    PC_cellNumber = 0
    for objPC in bpy.context.scene.objects:    
        if objPC.type == 'MESH' and objPC.name.startswith("ShapeIndexedFaceSet"):
            objPC.name = "PC" + str(PC_cellNumber)
            plasmaCells.append(objPC)
            PC_1 = objPC
            current_obj = bpy.context.active_object 
            scene = bpy.context.scene
            bpy.ops.object.origin_set(type="GEOMETRY_ORIGIN")
            originalX = PC_1.location.x
            originalY = PC_1.location.y
            originalZ = PC_1.location.z
            originalEulerX = PC_1.rotation_euler.x
            originalEulerY = PC_1.rotation_euler.y
            originalEulerZ = PC_1.rotation_euler.z
            PC_cellNumber += 1
            numPlasmaCells = len(plasmaCells)
            print("Number of plasma cells: ", numPlasmaCells)
            PC_1.select = True
            bpy.context.scene.objects.active = PC_1
            for rotNum in range(1,numberOfRotations+1):
                bpy.ops.object.origin_set( type = 'ORIGIN_GEOMETRY' ) #shift the center so that the rotation is around the object's own origin
                PC_1.rotation_euler.x = originalEulerX + random.uniform(-rotationSize,rotationSize)
                PC_1.rotation_euler.y = originalEulerY + random.uniform(-rotationSize,rotationSize)
                PC_1.rotation_euler.z = originalEulerZ + random.uniform(-rotationSize,rotationSize)
                if refreshScene == True:
                    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
                """ positioning the camera and rendering: """
                obj_camera = bpy.data.objects["Camera"]
                obj_other = bpy.data.objects["PC0"]
                obj_camera.location = camera_location 
                look_at(obj_camera, obj_other.matrix_world.to_translation())
                output_name = full_path_to_pc + output_filenameTag + '_'  + "rotNum_" + str(rotNum)
                bpy.context.scene.render.filepath = output_name
                if changeObjectColor == True:
                    bpy.context.object.active_material.diffuse_color = newObjectColor
                bpy.ops.render.render(animation=False, write_still=True, use_viewport=False, layer="", scene="")
                """ end of rendering""" 
                
            """Now remove the object so that the next one will be alone: """
            if deleteCellPerCycle == True:
                bpy.ops.object.select_all(action='DESELECT')
                for objSim in bpy.context.scene.objects:
                    if objSim.type == 'MESH' and objSim.name.startswith("PC"):
                        objSim.select = True
                        bpy.ops.object.delete()   
            
"""Delete all meshes at the end, ready for next image"""      
if deleteAllAtEnd == True:
    bpy.ops.object.select_all(action='DESELECT')
    for objAll in bpy.context.scene.objects:
        if objAll.type == 'MESH':
            objAll.select = True
            bpy.ops.object.delete()

if addSecondLamp == True:
    bpy.data.objects['Sun'].select = True
    bpy.ops.object.delete() 
        
print("Done with all ",numberOfRotations," rotations at ",time.strftime("%X") )
