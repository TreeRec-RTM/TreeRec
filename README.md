TreeRec
=========================================================================================================================
The algorithm places 3D shoot or leaf objects within a tree crown in a biologically realistic manner and merges them with a Quantitative Structure Model (QSM) of woody components. Placement is guided by Terrestrial Laser Scanning (TLS) data, leaf angle distribution (LAD), and leaf area index (LAI). Once the positions and orientations of all shoot or leaf objects are computed, the algorithm generates a single 3D foliage object and integrates it with the QSM, producing a merged 3D representation with distinct subgroups for wood and foliage.

For more details see Janoutová et al. 2019, 2021

-------------------------------------------------------------------------------------------------------------------------
**data**
- Test data of two Norway spruce trees (R1 and R2), which is working with the present form of the code.
- Data set includes:
  	- input files:
    		- wood component point cloud (R*_*_w)
 		- foliage point cloud (R*_*_l)
  		- quantitative structure model (QSM) made by Sloup (2013) (R*_wooden_parts_filled.obj)
    		- 3D shoot objects - folder **shoots**
   	- output files (folder scaled_cca_18m_LAI12):
   	 	- information about exact location and rotation of each shoot model for two groups of foliage: current and older (R*_shoot_distribution_*.csv)
   	  	- transformed QSM in 3D objet format (R*_wooden_parts_filled_scaled.obj)
   	  	- 3D object of the whole reconstructed tree - ready for Radiative Transfer Modelling (RTM) applications (R*_whole_tree_simple.obj)
- More information about trees and data acquisition you can find in Janoutová et al. 2019.
-------------------------------------------------------------------------------------------------------------------------
**scripts**
- Additional python scripts, which can be used for preparation of your data in the same input format as is necessary for TreeRec algorithm
- files:
  	- extract_FSCT_output_to_one_folder.py -> extracting segmented files (segmented.las) into one folder and rename them by tree id
   	- segmented_trees_to_foliage_reconstruction.py -> create three separate objects (wood point cloud, wood point cloud for QSM reconstruction and foliage point cloud) in file formats that are used in QSM reconstruction and main part of TreeRec algorithm
   	- AdQSM_to_XZY_00.py -> rotate and shift AdQSM OBJ file into XZY coordinates, and shift it to 0,0 coordinates
-------------------------------------------------------------------------------------------------------------------------
**segmentation_model**
- Forest Structural Complexity Tool (FSCT - https://github.com/SKrisanski/FSCT) adapted to Central European data, without coarse woody debris class
-------------------------------------------------------------------------------------------------------------------------
treerec
=========================================================================================================================
- The main part of the TreeRec algorithm.
-------------------------------------------------------------------------------------------------------------------------
**dependency list**
- You can find a dependency list here - dependency_list.txt
-------------------------------------------------------------------------------------------------------------------------
**input data:**
- separated wood component and foliage point clouds
	- it is possible to have only one file for foliage and one file for wooden components point cloud, but also it is possible to have multiple files, for example from different scanning position, but it has to be co-registered
	- format of the file name for the foliage/leaves - $treeID_*_l (R1_F-1_l)
	- format of the file name for the wooden components - $treeID_*_w (R2_F-2_w)
- QSM (3D object) - only wooden components
	- Check the correct direction of facet normals - It is necessary for RTM applications to check the normals of the facets (the right direction - it could be done in Blender).
 	- Check if 3D object is closed object - for RTM applications it is also necessary that there are no light traps (open cylinders etc.) - can be done in blender with function _fill_.
- 3D shoot/leaf model
-------------------------------------------------------------------------------------------------------------------------
**output data:**
- distribution file with calculated exact location and rotation of each 3D shoot/leaf object for current and older foliage (in case of coniferous species)
- scaled QSM (3D object)
- 3D object of the whole tree (foliage + wood)
-------------------------------------------------------------------------------------------------------------------------
**scripts**
- Main.py
 	- thi algorithm compute the positions and rotations of each 3D shoot/leaf objects within the tree crown
  	- input parameters to be set:
 		- path and name of input and output files
   		- list of trees for processing - their IDs (e.g., R1 or R2)
       		- the required height you want your final model to be scaled to - if set 0 the 3D object will have the same dimensions as the original tree
         	- tree LAI value, note that the canopy LAI (usually measured in field) would be lower
          	- technical parameters (d_cube, env_cube_size) for tuning of the distribution of leaf objects
          	- shoot or leaf object area - need to be set correctly. Based on this parameter and tree LAI is computed the total number of the 3D shoot/leaf objects
 	- this script is able to process several trees in one run
	- there are three possibilities how to set a leaf object or objects
		1) single leaf - 'single_leaf'
			- The tree crown will contain only one leaf object, which will vary only sligthly in the size
				- The area of this leaf has to be the same as set in the (Main.py)
			- If you select this option, then you need to set your leaf object name on line 33
		2) three leaves - 'three_leaves'
			- The tree crown will contain three different leaf objects: one represents average leaf (in terms of area),
				 one smaller and one larger.
				- There will be 50% of average leaves and 25% of smaller and 25% of larger leaves
				- The average (50% average, 25% smaller and 25% of larger) leaf area has to be the same
					as set in the (Main.py)
				- The size of all leaf objects will also sligthly vary
			- if you select this option, then you need to set your leaf object names on lines 25-27
		3) multiple leaves - 'multiple_leaves'
			- The tree crown will contain all the leaf objects you set here
				- The average leaf area of all leaves set here has to be the same as set in the (Main_beech_TH.py)
				- The size of all leaf objects will also vary
			- If you select this option, then you need to set your leaf object names on line 30
- main_classes.py
	- library of classes
------------------------------------------------------------------------------------------------------
**References:**

Janoutová, R., Homolová, L., Malenovský, Z., Hanuš, J., Lauret, N., & Gastellu-Etchegorry, J.-P. (2019). Influence of 3D Spruce Tree Representation on Accuracy of Airborne and Satellite Forest Reflectance Simulated in DART. Forests, 10(3), 35. https://doi.org/10.3390/f10030292

Janoutová, R., Homolová, L., Novotný, J., Navrátilová, B., Pikl, M., & Malenovský, Z. (2021). Detailed reconstruction of trees from terrestrial laser scans for remote sensing and radiative transfer modelling applications. In Silico Plants, 3(2). https://doi.org/10.1093/insilicoplants/diab026

Sloup, P. (2013). Automatic Tree Reconstruction from its Laser Scan [Diploma Thesis]. MASARYK UNIVERSITY FACULTY OF INFORMATICS. Available online: https://is.muni.cz/th/325196/fi_m/?lang=en

