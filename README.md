# ShapeAnalysis
Fiji plugin for DFT based shape factor calculation.  

Here you find the Python code "AutoRotate_v1.0.py" to perform automated rotation of VRML surfaces (.wrl files).
The code runs inside Blender 2.75a as a script.
Also inluded here is a Blender file "AutoRotate_v1.0.blend" with the Python script already embedded.
This work is available as a paper in Cytometry A 2017, by Kriegel et al.  

The Python script offers the user two different choices for the automatic creation of the cell surfaces in 2D inside Blender. If the user wants to focus on details of the cellular surface, it is recommended to use the script with the Lamp option ON. When the main focus is on the bare outlines of the cell, the lamp should be turned OFF. The script is able to search a user-specified folder structure for certain keywords. All files within the folder structure that match the keywords are then analyzed by the script using Blender. Each surface is centered, rendered and randomly rotated in all three dimensions 6 times (changeable inside the script). After each rotation, an image of the cell surface is generated. Example videos of the script with and without light source are supplied in our paper in Cyto,metry A, 2017 for a better understanding of the working principle of the script.  

The files named SHADExxx are part of the Fiji plugin that calculates the DFTs. For unaltered use, simply copy the jar file
into the "plugins" folder of your local Fiji installation. The .java file contains the source code, the .class file is its 
binary compiled version.

The trainSOM.m file can be run in Matlab to produce the trained SOM. It requires a simple .csv file, with the feature vector as
rows and the individual inputs (e.g., cells or cell tracks) as columns. E.g., with 8 track parameters and 1100 tracks (cells),
the input .csv file has to have 8 rows and 1100 columns.

Both for unaltered and altered use, please quote our work. Details are to be found in the header of each source code file.

