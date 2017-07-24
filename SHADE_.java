/*
 * SHADE  (Shape Data Evaluation) plugin for ImageJ/Fiji
 * 
 * Copyright (C) 2017 Ralf Köhler(1), Fabian Kriegel(2) and Dr. Zoltán Cseresnyés
 * 
 * (1) German Rheumatism Research Centre Berlin, Immune Dynamics
 * (2) German Federal Institute for Risk Assessment, Department of Chemical and Product Safety
 * (3) Hans Knöll Institute Jena, Applied Systems Biology
 * 
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation (http://www.gnu.org/licenses/gpl.txt )
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public
 * License along with this program.  If not, see http://gnu.org/licenses/gpl.html
 * 
 * */


import java.awt.Polygon;
import java.io.File;

import ij.IJ;
import ij.ImagePlus;
import ij.Prefs;
import ij.gui.GenericDialog;
import ij.gui.PolygonRoi;
import ij.gui.Roi;
import ij.gui.WaitForUserDialog;
import ij.measure.Measurements;
import ij.measure.ResultsTable;
import ij.plugin.PlugIn;
import ij.plugin.filter.Analyzer;
import ij.plugin.frame.RoiManager;
import ij.process.ImageConverter;
import ij.process.ImageProcessor;

/*
 * This Plugin was developed to characterize the shape in 2D projections of 3D cell images
 * recorded with a two photon microscope in discrete fourier transformed components. In
 * just a few components (we used 20) the whole shape can be saved and reproduced within 
 * a small memory usage. Special shape properties are visible insight these values. With all
 * components a database can be build creating machine learning approaches.
 * 
 * For more information you can read in following publication:
 * Cell shape characterization and classification with discrete
 * Fourier transforms and Self-Organizing Maps - Fabian L. Kriegel et al.; (Cytometry, Part A)
 * 
 * */
 
public class SHADE_  implements PlugIn {
	
		//initialize the global variables
		boolean checkbatch, checkintermediate, checkSave, checkDarkBackground;
		double numbergradient, iterationnumber, dilatations;
		int checkintermediate_wert;
		String dir2, imageName;
		ResultsTable bigResultsTable = new ResultsTable();
		
	public void run(String arg) {

		//graphical user interface for user defined values
		GenericDialog gd = new GenericDialog("SHADE"); // open Dialogwindow with Title "SHADE" 
		
		gd.addMessage("Set up the SHADE for finding edges");
		gd.addMessage("------------------------------------------");
		//gd.addCheckbox("Step-by-Step-Mode (manualy saving) ?",false);
		gd.addNumericField("Enter gradient threshold  ",40,0);
		gd.addNumericField("Enter number of iterations",25,0);
		gd.addNumericField("Number of dilatations", 10, 0);
		gd.addCheckbox("Dark Background?", false);
		gd.addCheckbox("Do you want to see the intermediate results ?", true);
		gd.addCheckbox("Do you want to save Result Tables?", true);
		gd.showDialog();

		if(gd.wasCanceled()) return;  
  
		numbergradient = gd.getNextNumber();
		iterationnumber = gd.getNextNumber();
		dilatations = gd.getNextNumber();
		checkDarkBackground = gd.getNextBoolean();
		checkintermediate = gd.getNextBoolean();
		checkSave = gd.getNextBoolean();

		if(checkintermediate==true) 
		checkintermediate_wert=1; 
		else checkintermediate_wert=0;
		
		// get directory of single cell images (tif file format required)
		String dir1 = IJ.getDirectory("Choose Source Folder"); 
		if(dir1 == null) return;
		String[] list1 = new File(dir1).list();
		if(list1 == null) return;
		IJ.log("image source folder: "+dir1);
		
		// get saving directory if option is checked
		if(checkSave==true){
			dir2 = IJ.getDirectory("Choose Results saving folder");
			IJ.log("Results Table saving folder: "+dir2);
		}
		
		int[] roiLoc = new int[4];
		
		// loop through every image and process
		for (int l = 0; l < list1.length; l++) {
			
			if(list1[l].endsWith(".tif")){
			
				IJ.open(dir1+list1[l]);
			
				ImagePlus img = IJ.getImage();
				imageName = img.getShortTitle();
			
				// first image is used to get user defined ROI
				//if(l==0)roiLoc = getInputROI(img);
				if(!ROIisSet(roiLoc)) roiLoc = getInputROI(img);
				img.setRoi(roiLoc[0],roiLoc[1],roiLoc[2],roiLoc[3]);
			
				//run absnake plugin with preprocessed images
				startPreprocess(img);
				ResultsTable rt = new ResultsTable();
				rt = getABSnakeCoordsAndCalc(img.getTitle());
			
				if(checkintermediate==true)
				rt.show("Results of : " + list1[l]);
			
				if(checkSave==true)
				rt.save(dir2+"Results_of_DFT_calc_"+(l+1)+"_"+imageName+".csv");
				IJ.run("Close All", "");
			
			}

		}
			
		bigResultsTable.show("All DFT components");
		if(checkSave==true) bigResultsTable.save(dir2+"Result_collection_of_all_DFT_calculations.csv");
		IJ.error("DFT calculations are done");
	}
	
	// check if ROI is set in a first image event
	public boolean ROIisSet(int[] roiLoc){
		
		if(roiLoc[0]>0 && roiLoc[1]>0 && roiLoc[2]>0 && roiLoc[3]>0){
			return true;
		}
		
	    return false;
	}
	
	// create ROI only around cell -> uninteresting parts will be cropped
	public int[] getInputROI(ImagePlus img) {
		
		ResultsTable rt = new ResultsTable();
		int measurements = Measurements.RECT;
		Analyzer analyzer = new Analyzer(img, measurements, rt);
		int[] roiPosition = new int[4];
				
		new WaitForUserDialog("First Image Event", "draw "
				+ "rectangle surounding cell !\n"
				+ "then you can go on by clicking 'OK' ").show();
		
		RoiManager rm = RoiManager.getInstance(); 
		if(rm==null) rm = new RoiManager();
		rm.addRoi(img.getRoi());
		analyzer.measure();
		roiPosition[0] = (int)rt.getValue("BX", 0);
		roiPosition[1] = (int)rt.getValue("BY", 0);
		roiPosition[2] = (int)rt.getValue("Width", 0);
		roiPosition[3] = (int)rt.getValue("Height", 0);
		img.deleteRoi();
		rm.select(0);
		rm.runCommand(img,"Deselect");
		rm.runCommand(img,"Delete");
		
		return roiPosition;
	}
	
	// crop image, make selection and run absnake plugin adding results to ROI manager
	public void startPreprocess(ImagePlus img){
		
		ImagePlus inputImg = img.crop();
		img.close();
		ImageConverter cv = new ImageConverter(inputImg);
		cv.convertToGray8();
		
			if (!checkDarkBackground) {
				IJ.setAutoThreshold(inputImg, "RenyiEntropy");
			}
			else {
				IJ.setAutoThreshold(inputImg,  "RenyiEntropy dark");
			}
			
		Prefs.blackBackground = false;
		IJ.run(inputImg, "Convert to Mask", "");
		
		ImagePlus duplImg = inputImg.duplicate();
		ImageProcessor ipDupl = duplImg.getProcessor();

		for(int i = 0; i<dilatations; i++) {
			ipDupl.dilate();
		}
		
		inputImg.deleteRoi();
		duplImg.deleteRoi();
		IJ.run(duplImg, "Create Selection" ,"");  
		Roi roi = duplImg.getRoi();
		
		Polygon p = roi.getPolygon();
		inputImg.setRoi(new PolygonRoi(p.xpoints,p.ypoints,p.npoints,Roi.POLYGON));

		duplImg.close();
		RoiManager rm = RoiManager.getInstance(); 
		if(rm==null) rm = new RoiManager();
		rm.addRoi(inputImg.getRoi());
		inputImg.show();
		
		IJ.run("ABSnake", "gradient_threshold="+numbergradient+" number_of_iterations="
		+iterationnumber+" step_results_show ="+checkintermediate_wert+" draw_color=Red save_coords");
		
		rm.select(0);
		rm.runCommand(img,"Deselect");
		rm.runCommand(img,"Delete");
		
		inputImg.close();
			
	}

	// read results from absnake txt file, calculate DFT components and add to Results Table
	public ResultsTable getABSnakeCoordsAndCalc(String imageTitle) {

		
		String pathfile = "ABSnake-r1-z1.txt"; 
		String filestring = IJ.openAsString(pathfile); 
		String[] rows = filestring.split("\n");
		//String[] title_row = rows[0].split("\\s+");  
		
		float[] num = new float[rows.length]; 
	   	float[] x = new float[rows.length];
		float[] y = new float[rows.length];
		float[] z = new float[rows.length];
		float[] xcal = new float[rows.length];
		float[] ycal = new float[rows.length];
	
			for (int r=1; r<rows.length; r++)  
			{									
			String[] data = rows[r].split("\\s+"); 
			String number = data[0];
			num[r] = Float.parseFloat(number);
			String xvalue = data[1];
			x[r] = Float.parseFloat(xvalue);
			String yvalue = data[2];
			y[r] = Float.parseFloat(yvalue);
			String zvalue = data[3];
			z[r] = Float.parseFloat(zvalue);
			String xcali = data[4];
			xcal[r] = Float.parseFloat(xcali);
			String ycali = data[5];
			ycal[r] = Float.parseFloat(ycali);
				
			}
		
		int n = x.length; 
		double[] oreal = new double[n];
		double[] oimag = new double[n];
		double[] oAmpl = new double[n];
		String[] natemp = new String[20];
		double[] toreal = new double[20];
		double[] toimag = new double[20];
		double[] toAmpl = new double[20];
		double[] tnumber = new double[20];
		String name = "Fourier-Parameter";
		
			for (int k = 0; k < n; k++) 
			{  
			double creal = 0;
			double cimag = 0;
			
			for (int t = 0; t < n; t++) {  
				creal = creal + x[t]*Math.cos(2*Math.PI * t * k / n) + y[t]*Math.sin(2*Math.PI * t * k / n);
				cimag = cimag + -x[t]*Math.sin(2*Math.PI * t * k / n) + y[t]*Math.cos(2*Math.PI * t * k / n);
				}
			
			oreal[k] = creal;
			oimag[k] = cimag;
			oAmpl[k] = Math.sqrt(creal*creal + cimag*cimag);
			}

		double[] timepoint = new double [19]; double time = 0;
			
			for (int ti=0; ti<19; ti++)
			{ 	timepoint[ti] = time ; time = time+1;	}

		ResultsTable frt = new ResultsTable();

			for (int temc=1; temc < 20; temc++)
			{
				
			toreal[temc]=oreal[temc]; 
			toimag[temc]=oimag[temc];
			toAmpl[temc]=oAmpl[temc];
			natemp[temc]=name;
			tnumber[temc]=temc+1;

			String real_value = String.valueOf(toreal[temc]);
			String imag_value = String.valueOf(toimag[temc]);
			String ampl_value = String.valueOf(toAmpl[temc]);
			
			bigResultsTable.incrementCounter();
			bigResultsTable.addValue("Real", real_value);
			bigResultsTable.addValue("Imag", imag_value);
			bigResultsTable.addValue("Ampl", ampl_value);
			bigResultsTable.addValue("file name", imageTitle);
			frt.incrementCounter();
			frt.addValue("Real", real_value); // (first column, value column(r))
			frt.addValue("Imag", imag_value);
			frt.addValue("Ampl", ampl_value);
			
			}	

			bigResultsTable.incrementCounter();
			bigResultsTable.addValue("Real", 0);
			bigResultsTable.addValue("Imag", 0);
			bigResultsTable.addValue("Ampl", 0);
		//frt.show("Results");
		return frt;
	}
	
	public void buildBigResultsTable(String real, String imag, String ampl){
		

	}
	
}