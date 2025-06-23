#!/usr/bin/env python3
import csv
import os
import time
from tqdm import tqdm
from colorama import Fore, Back, Style

# in case of obj files: the coordinates are in order x, z, y. And all the files calculated from the obj files are the
# with the same order.

def find_max_z(coo_path):
    """
    Find maximum of z coordinates in obj file.
    @param coo_path: path to file when we want to find the maximum
    @return: coordinates of point with maximal z coordinate
    """
    t_file = open(coo_path, 'r')
    t_csv_file = csv.reader(t_file, delimiter=' ')
    t_max = -100
    for row in t_csv_file:
        if row[0] == 'v' and float(row[-2]) > t_max:
            t_max = float(row[-2])
            max_row = [float(row[1]), float(row[2]), float(row[3])]
    t_file.close()
    return max_row


def trans_coordinates(coo_old_path, coo_new_path, max_veg, max_ske, corr_coef):
    """
    Translate the coordinates of the vegetation to the coordinates of wooden part. Produce a file with changed
    coordinates.
    @param coo_old_path: path to the file which we want to translate
    @param coo_new_path: path to the file which was translated
    @param max_veg: voxel coordinates with max z value of vegetation voxels
    @param max_ske: voxel coordinates with max z value of wooden parts
    @param corr_coef: correction coefficient for z coordinate correction
    """
    t_file_r = open(coo_old_path, 'r')
    t_csv_file_r = csv.reader(t_file_r, delimiter=' ')
    t_file_w = open(coo_new_path, 'w')
    t_csv_file_w = csv.writer(t_file_w, delimiter=' ')
    coo_1 = (max_ske[0]) - (max_veg[0])
    coo_2 = (max_ske[1]) - (max_veg[1]) + corr_coef  # because the wooden parts ends lower then the vegetation
    coo_3 = (max_ske[2]) - (max_veg[2])
    vect = [coo_1, coo_2, coo_3]
    for row in t_csv_file_r:
        if row[0] == 'v':
            t_line = [row[0], float(row[1]) + vect[0], float(row[2]) + vect[1], float(row[3]) + vect[2]]
            t_csv_file_w.writerow(t_line)
        else:
            t_csv_file_w.writerow(row)
    t_file_r.close()
    t_file_w.close()


def scale_obj_file(s_coef, obj_path, scaled_obj_path):
    t_file_r = open(obj_path, 'r')
    t_csv_file_r = csv.reader(t_file_r, delimiter=' ')
    t_file_w = open(scaled_obj_path, 'w')
    t_csv_file_w = csv.writer(t_file_w, delimiter=' ')
    for row in t_csv_file_r:
        if row[0] == 'v':
            t_line = [row[0], float(row[1])*s_coef, float(row[2])*s_coef, float(row[3])*s_coef]
            t_csv_file_w.writerow(t_line)
        else:
            t_csv_file_w.writerow(row)
    t_file_r.close()


def transformation(m_setup, tree_name, required_height):
    #prev_version: def transformation(veg_path, ske_path, tree_name, required_height):
    """
    Create a obj file from all lidar ascii files with given tree name. Transform coordinates of the vegetation data as
    they are in the same place as the wooden skeleton of the tree.
    @param veg_path: Path to the vegetation files.
    @param ske_path: Path to the wooden skeleton file.
    @param tree_name: Name of the tree.
    @param required_height: Height, to which we want to scale the final tree
    @return: max_veg
    """
    print(Back.BLUE+'Transformation of original point cloud:'+Style.RESET_ALL)
    start_time = time.time()
    print(m_setup.source_dir)
    list_veg_path, list_woo_path = m_setup.get_files(tree_name, m_setup.source_dir)
    list_veg_path.sort() # for the right order in paralel for cycle
    list_woo_path.sort()
    veg_all_path = os.path.join(m_setup.source_dir, tree_name + '_all.obj')
    veg_all_file = open(veg_all_path, 'w')
    max_skeleton = find_max_z(m_setup.wooden_obj_orig_path)
    if required_height == 0:
        scale_coef = 1
    else:
        scale_coef = required_height/max_skeleton[1]
    scale_obj_file(scale_coef, m_setup.wooden_obj_orig_path, m_setup.wooden_obj_fin_path)
    max_wooden = [0, 0, 0] # will be the final height of the wooden parts point cloud
    max_corr_coef = 0
    if len(list_veg_path) == len(list_woo_path):
        for woo_file, veg_file in tqdm(zip(list_woo_path, list_veg_path)):
            if woo_file.split('-')[:-1] != veg_file.split('-')[:-1]:
                print('The file ' + woo_file + ' or ' + veg_file + ' doesn\'t have corresponding file.')
                exit()
            try:
                b_woo_path = os.path.join(m_setup.source_dir, woo_file + '_orig.obj')
                max_woo = find_max_z(b_woo_path) # is max height of the single file of wooden parts point cloud (if there are multiple scans from TLS scanning)
                if max_wooden[1] < max_woo[1]:
                    max_wooden = max_woo
            except TypeError:
                pass # eh... I can't remember, what exactly is this catching
            try:
                l_veg_path = os.path.join(m_setup.source_dir, veg_file)
                b_veg_path = l_veg_path + '_orig.obj' # lidar file tranformed to obj format
                b_veg_trans_path = l_veg_path + '_trans.obj' # original data transposed to the same coordinates as the wooden skeleton
                b_veg_scale_path = l_veg_path + '.obj' # transposed data scaled to recquired height
                max_vegetation = find_max_z(b_veg_path) 
                corr_coef = max_vegetation[1] - max_wooden[1]
                if max_corr_coef < corr_coef:
                    max_corr_coef = corr_coef
                trans_coordinates(b_veg_path, b_veg_trans_path, max_vegetation, max_skeleton, corr_coef)
                scale_obj_file(scale_coef, b_veg_trans_path, b_veg_scale_path)
                veg_file = open(b_veg_scale_path, 'r')
                veg_all_file.write(veg_file.read())
                veg_file.close()
            except TypeError:
                exit()
        veg_all_file.close()

        print('Final transformation of all files are done.')
        print('It takes %s seconds.' % (time.time()-start_time))
        print('--------------------------------------------------------------')
        return scale_coef*(max_skeleton[1]+max_corr_coef)
    else:
        print('The number of foliage files doesn\'t match with number of wooden files.')
        exit()
