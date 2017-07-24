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
turnOffLamps = False
addSecondLamp = True #2nd lamp positioned next to the camera so that each scene is illuminated
rotationSize = np.pi
numberOfRotations = 6
seededRandom = True
deleteAllAtEnd = False
deleteCellPerCycle = True
sleepTime = 0.0
refreshScene = True
printMessages = True
camera_location= (17.0, 15.0, 16.0)
output_filename = "/data/DATA/DRFZ_BoneMarrow/Rendered/Render_test"
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
#path = "/media/zoltan/Zoltan_Win_Linux/Sandra/BoneMarrow/SentOn__02_02_2017/170201_Surf_Zoltan/150701_16-17-46_analysed_newAlgo"
#path = "/data/DATA/DRFZ_BoneMarrow/testDataset"
#path = "/media/zoltan/Elements/DATA_Desktop/DRFZ_BoneMarrow/testDataset"
#path = "/data/DATA/DRFZ_BoneMarrow/3D_simulations/wrl_files/a__150305_d30_Exp2M1_kappa_16-23-51_deconv_flip_rot_crop_unchecked_checked_fewerPCs"
path = "/home/zoltan/Schreibtisch/Daten_sync/Software_Projects/Blender_projects/TestData/a__15-30-14_150311_Exp2_M1_IgM_deconv_flipped_cropped_unchecked_checked"

#Add a new lamp:
if addSecondLamp == True:
    bpy.ops.object.lamp_add(type='SUN', radius=1, view_align=False, location=camera_location, 
    layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.context.object.data.shadow_soft_size = 0.01
    bpy.context.object.data.cycles.cast_shadow = True

if turnOffLamps == True:
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
obj_list = [item for item in file_list if item[-3:] == 'wrl']
obj_list_cortex = [item for item in file_list if item[-7:] == '447.wrl']
obj_list_sinusoids = [item for item in file_list if item[-7:] == '593.wrl']
obj_list_arterioles = [item for item in file_list if item[-7:] == '655.wrl']
obj_list_plasmaCells = [item for item in file_list if item[-7:] == '525.wrl']

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
bpy.context.scene.render.image_settings.file_format='PNG' 
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
            for rotNum in range(0,numberOfRotations-1):
                bpy.ops.object.origin_set( type = 'ORIGIN_GEOMETRY' ) #shift the center so that the rotation is around the object's own origin
                PC_1.rotation_euler.x = originalEulerX + random.uniform(-rotationSize,rotationSize)
                PC_1.rotation_euler.y = originalEulerY + random.uniform(-rotationSize,rotationSize)
                PC_1.rotation_euler.z = originalEulerZ + random.uniform(-rotationSize,rotationSize)
                if refreshScene == True:
                    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
                """ positioning the camera and rendering: """
                #bpy.ops.view3d.view_selected()
                #bpy.ops.view3d.camera_to_view_selected()
                obj_camera = bpy.data.objects["Camera"]
                obj_other = bpy.data.objects["PC0"]
                obj_camera.location = camera_location 
                look_at(obj_camera, obj_other.matrix_world.to_translation())
                output_name = output_filename + '_' + str(numPlasmaCells) + '_' + "rotNum_" + str(rotNum)
                bpy.context.scene.render.filepath = output_name
                bpy.ops.render.render(animation=False, write_still=True, use_viewport=False, layer="", scene="")
                """ end of rendering""" 
                
            """Now remove the PC so that the next one will be alone: """
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

bpy.data.objects['Sun'].select = True
bpy.ops.object.delete() 
        
print("Done with all ",numberOfRotations," rotations at ",time.strftime("%X") )
