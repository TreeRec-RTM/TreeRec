#!/usr/bin/env python3
import os
from main_classes import Tree, general_setup
from colorama import Fore, Back, Style

home_dir = os.getcwd()
trees_arr = ['R2','R1']
shoot_name = 'PIABshoot0_one_shoot_simpl_bl' # name of the shoot/leaf object without .obj
shoot_type = 'simple' # it will apear in the file name of the whole tree 3D object
shoot_form = 'single_leaf' # all options: single_leaf, three_leaves, multiple_leaves - described below
height_arr = [18,15] # array of required_height = 18 for the tree R2 and 15 for R1,if is height set to 0, the tree dimensions will be preserved as original
shoot_area = 0.007604  # from object PIABshoot0_one_shoot_real_size_without_twig.obj
LAI_arr = [12,5] # array of LAI values per tree
note = '' # if you want to add some note to the folder name

# ## for original height cca 25
# d_cube = 0.3  # the diameter of the sphere, which will represent one cluster. It should be equal cca 30 cm.
# env_cube_size = 0.75
# required_height = 0

# ## for height 10
# d_cube = 0.12  # the diameter of the sphere, which will represent one cluster. It should be equal cca 12 cm.
# env_cube_size = 0.3

# ## for height 18 - after all modifications
d_cube = 0.075  # the diameter of the sphere, which will represent one cluster. It should be equal cca 7.5 cm.
env_cube_size = 0.5

## optional changed
# d_cube = 0.03  # the diameter of the sphere, which will represent one cluster. It should be equal cca 3 cm.
# env_cube_size = 0.05

# for Tree_name, sLAI in tree_set:
#     #Tree_name = 'tree_6'
#     vegetation_path = os.path.join(data_path, Tree_name)
#
#     if leaf_form == 'three_leaves':
#         leaf_name_ave = 'beech_leaf_simple.obj' # fill up name of your own average leaf object
#         leaf_name_sma = 'beech_leaf_simple_smaller.obj' # fill up name of your own smaller leaf object
#         leaf_name_big = 'beech_leaf_simple_larger.obj' # fill up name of your own larger leaf object
#         leaf_name_arr = [leaf_name_ave, leaf_name_sma, leaf_name_big]
#     elif leaf_form == 'multiple_leaves':
#         leaf_name_arr = ['beech_leaf_simple_1.obj','beech_leaf_simple_2.obj','beech_leaf_simple_3.obj','beech_leaf_simple_4.obj','beech_leaf_simple_5.obj']
#     else: # leaf_form == 'single_leaf' and also the default one
#         # leaf_name_arr = 'beech_leaf.obj'
#         #leaf_name_arr = 'beech_leaf_simple.obj'
#          #leaf_name_arr = 'maple_leaf_DART_rot.obj'
#          #leaf_name_arr = 'oak_leaf_1_simple.obj'
#          leaf_name_arr = 'birch_leaf_1_simple.obj'

source_dir = os.path.join(home_dir, 'data')
if not os.path.isdir(source_dir):
    print(Fore.YELLOW + 'The directory %s was not found.' % source_dir + Style.RESET_ALL )
else:
    for i_tree in range(len(trees_arr)):
        final_dir = os.path.join(home_dir,'data','scaled_cca_%sm_LAI%d%s' % (height_arr[i_tree], LAI_value, note))
        required_height = height_arr[i_tree]
        Tree_name = trees_arr[i_tree]
        mine_setup = general_setup(source_dir, final_dir, Tree_name, shoot_name, shoot_type)
        mine_tree = Tree(Tree_name, d_cube, shoot_area, LAI_value, env_cube_size, mine_setup)
        mine_tree.initiate_tree(required_height)
        mine_tree.create_tree_obj_file()
        del mine_setup, mine_tree
