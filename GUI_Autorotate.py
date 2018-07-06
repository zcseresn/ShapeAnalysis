# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 15:55:34 2018

@author: zoltan
"""

import bpy


class CustomDrawOperator(bpy.types.Operator):
    bl_idname = "object.custom_draw"
    bl_label = "Import"
 
    filepath = bpy.props.StringProperty(subtype="FILE_PATH")
 
    my_float = bpy.props.FloatProperty(name="Float")
    my_bool = bpy.props.BoolProperty(name="Toggle Option")
    my_string = bpy.props.StringProperty(name="String Value")
 
    def execute(self, context):
        print()
        return {'FINISHED'}
 
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
 
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text="Custom Interface!")
 
        row = col.row()
        row.prop(self, "my_float")
        row.prop(self, "my_bool")
 
        col.prop(self, "my_string")
 
bpy.utils.register_class(CustomDrawOperator)
 
# test call
#bpy.ops.object.custom_draw('INVOKE_DEFAULT')


# https://blender.stackexchange.com/q/57306/3710
# https://blender.stackexchange.com/q/79779/3710

bl_info = {
    "name": "Add-on Template",
    "description": "",
    "author": "",
    "version": (0, 0, 1),
    "blender": (2, 75, 0),
    "location": "3D View > Tools",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}

import bpy
import random
import os
import numpy as np
import time

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       PropertyGroup,
                       )

folderToRead = bpy.props.StringProperty()

# ------------------------------------------------------------------------
#    store properties in the active scene
# ------------------------------------------------------------------------

class MySettings(PropertyGroup):

    my_bool = BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default = False
        )

    num_rot = IntProperty(
        name = "Rotations",
        description="Number of rotations",
        default = 6,
        min = 6,
        max = 100
        )

    my_float = FloatProperty(
        name = "Float Value",
        description = "A float property",
        default = 23.7,
        min = 0.01,
        max = 30.0
        )
    
    my_float_vector = FloatVectorProperty(
        name = "Float Vector Value",
        description="Something",
        default=(0.0, 0.0, 0.0), 
        min= 0.0, # float
        max = 0.1
    ) 

    my_string = StringProperty(
        name="User Input",
        description=":",
        default="",
        maxlen=1024,
        )

    my_enum = EnumProperty(
        name="Dropdown:",
        description="Apply Data to attribute.",
        items=[ ('OP1', "Option 1", ""),
                ('OP2', "Option 2", ""),
                ('OP3', "Option 3", ""),
               ]
        )

# ------------------------------------------------------------------------
#    operators
# ------------------------------------------------------------------------

class RotateSetup(Operator):
    bl_idname = "wm.rotatesetup"
    bl_label = "Rotate!"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        #ar = AutoRotate()
        
        # print the values to the console
        print("Now preparing to rotate")
        print("Lights on:", mytool.my_bool)
        print("Number of rotations:", mytool.num_rot)
        print("float value:", mytool.my_float)
        print("string value:", mytool.my_string)
        print("enum state:", mytool.my_enum)
        #print("Object ID:", ar.GetSelf())
        #filename = '/home/zoltan/Documents/Daten_sync/Software_Projects/Blender_projects/Python_Blender_Scripts/AutoRotate_v1.0.py'
        #exec(compile(open(filename).read(), filename, 'exec'))
        #bpy.ops.object.custom_draw('INVOKE_DEFAULT')
        #folder = bpy.ops.object.custompath('INVOKE_DEFAULT')
        #bpy.ops.object.custompath('INVOKE_DEFAULT')#off, if called from AutoRotate itself
        print("Now rotating:", AutoRotate.rotate(mytool.num_rot, ''))
        #ar=AutoRotate()
        #ar.rotate(6)
        
	
        return {'FINISHED'}


# ------------------------------------------------------------------------
#    menus
# ------------------------------------------------------------------------

class BasicMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_select_test"
    bl_label = "Select"

    def draw(self, context):
        layout = self.layout

        # built-in example operators
        layout.operator("object.select_all", text="Select/Deselect All").action = 'TOGGLE'
        layout.operator("object.select_all", text="Inverse").action = 'INVERT'
        layout.operator("object.select_random", text="Random")

# ------------------------------------------------------------------------
#    my tool in objectmode
# ------------------------------------------------------------------------

class OBJECT_PT_my_panel(Panel):
    bl_idname = "OBJECT_PT_my_panel"
    bl_label = "Autorotate for SHADE"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "TOOLS"    
    bl_category = "Tools"
    bl_context = "objectmode"   

    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "my_bool")
        layout.prop(mytool, "my_enum", text="") 
        layout.prop(mytool, "num_rot")
        layout.prop(mytool, "my_float")
        layout.prop(mytool, "my_float_vector", text="")
        layout.prop(mytool, "my_string")
        layout.operator("wm.rotatesetup")
        layout.menu("OBJECT_MT_select_test", text="Presets", icon="SCENE")
        
# ------------------------------------------------------------------------
# register and unregister
# ------------------------------------------------------------------------

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.my_tool = PointerProperty(type=MySettings)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()


# ------------------------------------------------------------------------
# path finder:
# ------------------------------------------------------------------------

class custompath(Operator):
    bl_idname = "wm.custompath"
    #bl_idname = "custompath"
    bl_label = "Select wrl files"
    __doc__ = ""

    scene = bpy.context.scene
    mytool = scene.my_tool
    filename_ext = ".wrl"
    filter_glob = StringProperty(default="*.wrl", options={'HIDDEN'})

    my_float = bpy.props.FloatProperty(name="Float")
    my_bool = bpy.props.BoolProperty(name="Toggle Option")
    my_string = bpy.props.StringProperty(name="String Value")
    

    #this can be look into the one of the export or import python file.
    #need to set a path so so we can get the file name and path
    filepath = StringProperty(name="File Path", description="Filepath used for importing wrl files", maxlen= 1024, default= "")
    files = bpy.props.CollectionProperty(
        name="File Path",
        type=bpy.types.OperatorFileListElement,
        )    
    #print("1st file: ", files[0].name)
    @staticmethod
    def getPath(self):
        return self.properties.filepath
        
    def execute(self, context):
        #set the string path of the file here.
        #this is a variable created from the top to start it
        #bpy.context.scene.MyString = self.properties.filepath
        my_string = self.properties.filepath

        print("*************SELECTED FILES ***********")
        for file in self.files:
            print(file.name, '  ', my_string)

        print("FILEPATH1 %s"%self.properties.filepath)#display the file name and current path
        print("FILEPATH2 %s"%my_string.replace(file.name, ''))#display the file name and current path
        pathFolder = self.properties.filepath.replace(file.name, '')
        file = open('path.txt', 'w')
        print("Path to be written:", pathFolder)
        file.write(pathFolder)
        file.close()
        return {'FINISHED'}
        #return {self.properties.filepath.replace(self.files[0].name, '')}
        #return "test"#self.properties.filepath.replace(self.files[0].name, '')

    def draw(self, context):
        self.layout.operator('file.select_all_toggle')        
    
    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}
        #return self.properties.filepath.replace(self.files[0].name, '')
bpy.utils.register_class(custompath)



# ------------------------------------------------------------------------
#    Auto-rotate
# ------------------------------------------------------------------------

class AutoRotate(Operator):
    bl_idname="wm.rotate"
    bl_label="Auto rotate"
    bpy.ops.wm.custompath('INVOKE_DEFAULT')
    
    #print("Path from GUI: ", custompath.getPath())
    
    @staticmethod
    def rotate(num_rot, folder):
        """Users' data and other settings: """
        file = open('path.txt', 'r')
        for line in file:
            parts = line.split(' ')
        file.close()
        folderPath = parts[0]
        print("Path read from GUI inside rotate = ", folderPath)        
        
        fileFormat = 'TIFF'
        changeObjectColor = True
        newObjectColor = (0.0, 0.2, 0.0) #RGB 0.0-1.0, sum=1.0, use 0.1 each for dark grey
        turnOffLamps = False
        addSecondLamp = False #2nd lamp positioned next to the camera so that each scene is illuminated
        rotationSize = np.pi
        numberOfRotations = num_rot
        deleteAllAtEnd = True
        deleteCellPerCycle = True
        refreshScene = True
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
        path = "/home/zoltan/Documents/Daten_sync/Articles/MyPapers/Papers_under_preparation/JoVE_2018/Submitted/Data/RestingCells_smallSubset"
        if folderPath != '':        
            path = folderPath        
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
        obj_list_plasmaCells = [item for item in file_list if item[-3:] == 'wrl']
        
        print()
        print("# of files: ", len(obj_list_plasmaCells))
        
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
        return {'FINISHED'}
bpy.utils.register_class(AutoRotate)


