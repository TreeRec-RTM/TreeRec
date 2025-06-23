#!/usr/bin/env python3
import os
from geometric_op import create_shoot_obj_file
# from geometric_op import test_all

home_path = os.getcwd()
trees_dir = 'scaled_cca20m_LAI12'
vegetation_path = os.path.join(home_path, 'data', trees_dir)
s_path = os.path.join(home_path, 'data')
Tree_name = 'R2'
# d_cube = 0.3

# shoot_path = os.path.join(s_path, 'PIABshoot0_one_shoot_real_size.obj')
shoot_path_sep = os.path.join(s_path, 'PIAB_one_shoot_real_size_twig_needle_sep.obj')
# shoot_path_needle = os.path.join(vegetation_path, 'PIABshoot0_one_shoot_real_size_without_twig.obj')
# shoot_path_twig = os.path.join(vegetation_path, 'PIABshoot0_one_shoot_real_size_only_twig.obj')

# shoots_in_path = os.path.join(vegetation_path, Tree_name + '_shoots_in_objects.obj')
# shoots_edge_path = os.path.join(vegetation_path, Tree_name + '_shoots_edge_objects.obj')
#shoots_in_path_sep = os.path.join(vegetation_path, Tree_name + '_sep_shoots_in_objects.obj')
#shoots_edge_path_sep = os.path.join(vegetation_path, Tree_name + '_sep_shoots_edge_objects.obj')
# shoots_in_path_needle = os.path.join(vegetation_path, Tree_name + '_needle_shoots_in_objects.obj')
# shoots_edge_path_needle = os.path.join(vegetation_path, Tree_name + '_needle_shoots_edge_objects.obj')
# shoots_in_path_twig = os.path.join(vegetation_path, Tree_name + '_twig_shoots_in_objects.obj')
# shoots_edge_path_twig = os.path.join(vegetation_path, Tree_name + '_twig_shoots_edge_objects.obj')

shoot_path_simpl = os.path.join(s_path, 'PIABshoot0_one_shoot_simpl_bl.obj')
# shoot_path_simpl_1 = os.path.join(vegetation_path, 'PIABshoot0_one_shoot_simpl_1_bl.obj')
# shoot_path_simpl_2 = os.path.join(vegetation_path, 'PIABshoot0_one_shoot_simpl_2_bl.obj')
# shoot_path_simpl_2 = os.path.join(vegetation_path, 'PIABshoot0_one_shoot_simpl_2_bl.obj')
# shoot_path_simpl_2 = os.path.join(vegetation_path, 'PIABshoot0_one_shoot_simpl_2_bl.obj')
#
shoots_in_path_simpl = os.path.join(vegetation_path, Tree_name + '_simpl_shoots_in_objects.obj')
# shoots_in_path_simpl_1 = os.path.join(vegetation_path, Tree_name + '_simpl_1_shoots_in_objects.obj')
# shoots_in_path_simpl_2 = os.path.join(vegetation_path, Tree_name + '_simpl_2_shoots_in_objects.obj')

shoots_edge_path_simpl = os.path.join(vegetation_path, Tree_name + '_simpl_shoots_edge_objects.obj')
# shoots_edge_path_simpl_1 = os.path.join(vegetation_path, Tree_name + '_simpl_1_shoots_edge_objects.obj')
# shoots_edge_path_simpl_2 = os.path.join(vegetation_path, Tree_name + '_simpl_2_shoots_edge_objects.obj')
#
shoot_distr_in_path = os.path.join(vegetation_path, Tree_name + '_shoot_distribution_in.csv')
shoot_distr_edge_path = os.path.join(vegetation_path, Tree_name + '_shoot_distribution_edge.csv')
#

# #
# create_shoot_obj_file(shoots_in_path, shoot_distr_in_path, shoot_path)
# create_shoot_obj_file(shoots_edge_path, shoot_distr_edge_path, shoot_path)
#
#create_shoot_obj_file(shoots_in_path_sep, shoot_distr_in_path, shoot_path_sep)
#create_shoot_obj_file(shoots_edge_path_sep, shoot_distr_edge_path, shoot_path_sep)

# create_shoot_obj_file(shoots_in_path_needle, shoot_distr_in_path, shoot_path_needle)
# create_shoot_obj_file(shoots_edge_path_needle, shoot_distr_edge_path, shoot_path_needle)
#
# create_shoot_obj_file(shoots_in_path_twig, shoot_distr_in_path, shoot_path_twig)
# create_shoot_obj_file(shoots_edge_path_twig, shoot_distr_edge_path, shoot_path_twig)

create_shoot_obj_file(shoots_in_path_simpl, shoot_distr_in_path, shoot_path_simpl)
# create_shoot_obj_file(shoots_in_path_simpl_1, shoot_distr_in_path, shoot_path_simpl_1)
# create_shoot_obj_file(shoots_in_path_simpl_2, shoot_distr_in_path, shoot_path_simpl_2)

create_shoot_obj_file(shoots_edge_path_simpl, shoot_distr_edge_path, shoot_path_simpl)
# create_shoot_obj_file(shoots_edge_path_simpl_1, shoot_distr_edge_path, shoot_path_simpl_1)
# create_shoot_obj_file(shoots_edge_path_simpl_2, shoot_distr_edge_path, shoot_path_simpl_2)


# shoot_distr_path = os.path.join(vegetation_path)
# shoot_distr_path = os.path.join(vegetation_path, 'R2_LAI6_and_others_experiments', Tree_name + '_shoot_distribution')
# envelop_path = os.path.join(vegetation_path, 'R2_LAI6_and_others_experiments', Tree_name + '_envelop_finer.obj')


# shoot_distr_path = os.path.join(vegetation_path, 'distr_arr_test.txt')
# envelop_path = os.path.join(vegetation_path, 'env_arr_test.txt')
# # create_envelop_file(shoot_distr_path, envelop_path, d_cube)
#
# test_all(shoot_distr_path, envelop_path)
