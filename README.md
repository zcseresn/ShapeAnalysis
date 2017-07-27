# ShapeAnalysis
Fiji plugin for DFT based shape factor calculation.  

Here you find the Python code "AutoRotate_v0.8.py" to perform automated rotation of VRML surfaces (.wrl files).
The code runs inside Blender 2.75a as a script.
Also inluded here is a Blender file "AutoRotate_v0.8.blend" with the Python script already embedded.
This work is available as a paper in Cytometry A 2017, by Kriegel et al.  

The files named SHADExxx are part of the Fiji plugin that calculates the DFTs. For unaltered use, simply copy the jar file
into the "plugins" folder of your local Fiji installation. The .java file contains the source code, the .class file is its 
binary compiled version.

The trainSOM.m file can be run in Matlab to produce the trained SOM. It requires a simple .csv file, with the feature vector as
rows and the individual inputs (e.g., cells or cell tracks) as columns. E.g., with 8 track parameters and 1100 tracks (cells),
the input .csv file has to have 8 rows and 1100 columns.

Both for unaltered and altered use, please quote our work. Details are to be found in the header of each source code file.

