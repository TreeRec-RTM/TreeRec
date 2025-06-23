#!/usr/bin/env python3
import os
from main_classes import Tree, general_setup
from colorama import Fore, Back, Style

home_dir = os.getcwd()
#home_dir = '/media/janoutova/Elements/backup_ntb/home/Documents/scripts/disertation/'
home_dir = '/home/janoutova.r/Documents/TreeRec/'
trees_arr = ['R2','R1']
#shoot_name = 'PIAB_one_shoot_real_size_twig_needle_sep'
shoot_name = 'PIABshoot0_one_shoot_simpl_bl'
shoot_type = 'simple' # 'simple' # fpr example
height_arr = [18,18] # array of required_height = 13  # if is height set to 0, the height will be preserved as original
shoot_area = 0.007604  # from object PIABshoot0_one_shoot_real_size_without_twig.obj and shoot_area.ods
LAI_value = 12
note = '' # if you want to add some note to the folder name
# ## for original height cca 25
# d_cube = 0.3  # the diameter of the sphere, which will represent one cluster. It should be equal cca 30 cm.
# env_cube_size = 0.75
# required_height = 0

# ## for height 10
# d_cube = 0.12  # the diameter of the sphere, which will represent one cluster. It should be equal cca 12 cm.
# env_cube_size = 0.3

# ## for height 18 - after all modifications
d_cube = 0.075  # the diameter of the sphere, which will represent one cluster. It should be equal cca 18 cm.
env_cube_size = 0.5

## optional changed
# d_cube = 0.03  # the diameter of the sphere, which will represent one cluster. It should be equal cca 30 cm.
# env_cube_size = 0.05

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
