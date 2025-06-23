======================================================================================================
General ReadMe
======================================================================================================
scripts
------------------------------------------------------------------------------------------------------

processing:
- data was separated into two parts: wooden and foliage point cloud
- Sloup algorithm (or AdQSM, TreeQSM or another) was applied to the wooden point cloud -> wooden structure was made
- it is necessary to check if the normals of the facets are set the right way (it could be done in Blender).
- the wooden structure object was filled/closed (the algorithm generate set of truncated cones
	without closed top and bottom parts) - in blender if function fill -> filled wooden
	structure object is made
- application of RJ algorithm (Main_beech_TH.py)
	- this script is able to process several trees in one run
	- parameters necessary to set are:
		- id/name of the tree (variable trees_arr - line 9)
		- required height - the height required for the tree model (variable height_arr line 16)
		- LAI value (variable LAI_arr line 23)
		- area of leaf object - necessary for getting the right LAI (number of leaf objects in the tree crown
			according to LAI value)
		- size of cubes for computation of leaf positions (the env_cube_size is probably redundant - it is not cleared after
			adaptation from the spruce version of the script)
		-> the output of this part of the algorithm is scaled wooden structure object, .csv
			file with coordinates of leaf objects and the information about their rotation.
- application of RJ algorithm (get_new_shoots_TH.py)
	- this algorithm distribute leaf objects within the tree crown according to the leaf distribution file
		generated in previous step
	- parameters necessary to set are:
		- directory of the files computed in the previous step (the location of leaf positions) - leaf distribution file
		- tree id/name
		- here is possible to set the leaf object for creating the 3D model of the tree
			- there are three possibilities how to set a leaf object or objects (line 16-18)
				1) single leaf - 'single_leaf'
					- The tree crown will contain only one leaf object, which will vary only sligthly in the size
						(see line 695 in geometric_op_TH.py)
						- The area of this leaf has to be the same as set in the (Main_beech_TH.py)
					- If you select this option, then you need to set your leaf object name on line 33
				2) three leaves - 'three_leaves'
					- The tree crown will contain three different leaf objects: one represents average leaf (in terms of area),
						 one smaller and one larger.
						- There will be 50% of average leaves and 25% of smaller and 25% of larger leaves
						- The average (50% average, 25% smaller and 25% of larger) leaf area has to be the same
							as set in the (Main_beech_TH.py)
						- The size of all leaf objects will also sligthly vary (see line 695 in geometric_op_TH.py)
					- if you select this option, then you need to set your leaf object names on lines 25-27
				3) multiple leaves - 'multiple_leaves'
					- The tree crown will contain all the leaf objects you set here
						- The average leaf area of all leaves set here has to be the same as set in the (Main_beech_TH.py)
						- The size of all leaf objects will also vary (see line 695 in geometric_op_TH.py)
					- If you select this option, then you need to set your leaf object names on line 30
		- for better implementation of tree models in DART (for example) put together all the objects
			(wooden structure and leaf object part of the tree in blender - import all the object in blender
			and save them as one object with separated groups -> one object file with all the parts of the tree
			- this is now possible to do in python directly, but it is not implemented yet
======================================================================================================
Specification for different species
======================================================================================================
European beech (Fagus sylvatica)
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- the LAD is based on planophil LAD function (file LAD_plano.txt)
	- if needed - the name and path of the file is need to be changed in script (geometric_op_TH.py line 169)
- the normals of leaf object has to be recalculated (it is a function in Blender) in Blender, so that all
the normals are face up.
------------------------------------------------------------------------------------------------------
