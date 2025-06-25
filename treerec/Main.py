#!/usr/bin/env python3
import os
# from pathlib import Path # update with this library
from main_classes import Tree, general_setup, Leaf
from colorama import Fore, Back, Style

home_dir = os.getcwd()
data_dir = os.path.abspath(os.path.join(home_dir,'..','data'))
leaf_dir = os.path.join(data_dir,'shoots_&_leaves')
QSM_dir = data_dir
QSM_base_name = '_wooden_parts_filled.obj' # the full name should be R1_wooden_parts_filled.obj or R2_wooden_parts_filled.obj where, R1 and R2 are the tree IDs

trees_arr = ['R2','R1'] # point clouds foliage and wooden commponents have to be in format treeID_*_l - foliage/leaves or treeID_*_w - wooden components
# leaf_name = 'PIABshoot0_one_shoot_simpl_bl' # name of the shoot/leaf object without .obj
leaf_type = 'simple' # it will apear in the file name of the whole tree 3D object
leaf_form = 'single_leaves' # all options: single_leaf, three_leaves, multiple_leaves - described below
current_shoots = True # True for generating shoots in two age categories (current and older ones) -> two set of object groups; False if all the leaves/shoots will be in the same age -> one object group
# LAD_type = 'spruce' # based on measured data Janoutova et al. 2019 not prepared for other species
LAD_type = 'file' # if you want to use a LAD (leaf angle distribution) defined by file
LAD_dir = home_dir # the directory where the LAD file is placed
LAD_file = 'LAD_plano.txt' # the name of the LAD file
height_arr = [18,15] # array of required_height = 18 for the tree R2 and 15 for R1,if is height set to 0, the tree dimensions will be preserved as original
leaf_area = 0.007604  # from object PIABshoot0_one_shoot_real_size_without_twig.obj
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

if leaf_form == 'three_leaves':
    leaf_name_ave = 'beech_leaf_simple.obj' # fill up name of your own average leaf object
    leaf_name_sma = 'beech_leaf_simple_smaller.obj' # fill up name of your own smaller leaf object
    leaf_name_big = 'beech_leaf_simple_larger.obj' # fill up name of your own larger leaf object
    leaf_name_arr = [leaf_name_ave, leaf_name_sma, leaf_name_big]
elif leaf_form == 'multiple_leaves':
    leaf_name_arr = ['beech_leaf_simple_1.obj','beech_leaf_simple_2.obj','beech_leaf_simple_3.obj','beech_leaf_simple_4.obj','beech_leaf_simple_5.obj']
else: # leaf_form == 'single_leaf' and also the default one
    leaf_name_arr = 'beech_leaf_simple.obj'
    # leaf_name_arr = 'PIABshoot0_one_shoot_simpl_bl.obj'

source_dir = os.path.join(data_dir)
if not os.path.isdir(source_dir):
    print(Fore.YELLOW + 'The directory %s was not found.' % source_dir + Style.RESET_ALL )
else:
    for i_tree in range(len(trees_arr)):
        LAI_value = LAI_arr[i_tree]
        final_dir = os.path.join(data_dir,'scaled_cca_%sm_LAI%d%s' % (height_arr[i_tree], LAI_value, note))
        required_height = height_arr[i_tree]
        tree_name = trees_arr[i_tree]
        mine_leaf = Leaf(leaf_dir, leaf_name_arr, leaf_area, leaf_form)
        # mine_setup = general_setup(source_dir, final_dir, tree_name, leaf_name, leaf_type)
        mine_setup = general_setup(source_dir, QSM_dir, QSM_base_name, final_dir, tree_name, leaf_type, current_shoots)
        # mine_tree = Tree(tree_name, d_cube, leaf_area, LAI_value, env_cube_size, mine_setup)
        mine_tree = Tree(tree_name, d_cube, LAI_value, env_cube_size, mine_setup, mine_leaf)
        mine_tree.initiate_tree(required_height)
        mine_tree.create_tree_obj_file()
        del mine_setup, mine_tree
