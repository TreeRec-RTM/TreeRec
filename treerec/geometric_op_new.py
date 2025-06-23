import csv
from math import *
from random import uniform
import numpy as np
from scipy.cluster.vq import kmeans
import os
import time
from tqdm import tqdm
import itertools
from colorama import Fore, Back, Style
from joblib import Parallel, delayed
import multiprocessing
from datetime import timedelta

# in case of obj files: the coordinates are in order x, z, y. And all the files calculated from the obj files are the
# with the same order.

#def load_voxels(veg_path, tree_name):
    #"""
    #Load the list of voxels representing the vegetation voxels.
    #@param veg_path: Path to the file with voxel coordinates.
    #@param tree_name: Name of the tree.
    #@return: List of the voxels. It means list of voxel coordinates.
    #"""
    #print(Back.BLUE+'Loading voxels:'+Style.RESET_ALL)
    #start_time = time.time()
    #t_file_name = os.path.join(veg_path, tree_name+'_all.obj')
    #t_file = open(t_file_name, 'r')
    #t_csv_file = csv.reader(t_file, delimiter=' ')
    #vox_arr = []
    #for row in tqdm(t_csv_file):
        #if row[0] == 'v':
            #vox_arr.append([float(row[1]), float(row[2]), float(row[3])])
    #t_file.close()
    #print('Load voxels from ' + t_file_name + ' - done.')
    #print('It takes %s seconds.' % (time.time()-start_time))
    #print('--------------------------------------------------------------')
    #return vox_arr


def load_voxels_from_distr(distr_path):
    """
    Load the voxels from distribution file. This voxels represent the position of the needle shoots.
    Using only for testing.
    @param distr_path: Path to the file with voxel coordinates.
    @return: List of the voxels. It means list of voxel coordinates.
    """
    print(Back.BLUE+'Loading voxels:'+Style.RESET_ALL)
    start_time = time.time()
    t_file_name = os.path.join(distr_path)
    t_file = open(t_file_name, 'r')
    t_csv_file = csv.reader(t_file, delimiter=' ')
    vox_arr = []
    for row in tqdm(t_csv_file):
        vox_arr.append([float(row[0]), float(row[1]), float(row[2])])
    t_file.close()
    print('Load voxels from ' + t_file_name + ' - done.')
    print('It takes %s seconds.' % (time.time()-start_time))
    print('--------------------------------------------------------------')
    return vox_arr


def load_voxels_from_envelop(veg_path):
    """
    Load the list of voxels representing the envelop. Using only for testing.
    @param veg_path: Path to the file with voxel coordinates.
    @return: List of the voxels. It means list of voxel coordinates.
    """
    t_file = open(veg_path, 'r')
    t_csv_file = csv.reader(t_file, delimiter=' ')
    vox_arr = []
    for row in tqdm(t_csv_file):
        if row[0] == 'v':
            vox_arr.append([float(row[1]), float(row[2]), float(row[3])])
    t_file.close()
    return vox_arr


#def find_projection_area(vox_arr):
    #"""
    #Return an area of the circle projection along z axis, where lies 90 % of all voxels. The center of the circle
    #doesn't lies in the origin of the tree coordinates. The radius of the circle is set as
    #min((max_x-min_x),(max_y-min_y)). Where min_x is minimal x coordinate of 90 % of voxels. max_x, min_y, max_y
    #is calculated similarly.
    #@param vox_arr: list tof all voxels
    #@return: area of the projection along the z axis
    #"""
    #print(Back.BLUE+'Computing projection area:'+Style.RESET_ALL)
    #start_time = time.time()
    #d_arr=[]
    #for i_vox in tqdm(vox_arr):
        #d = sqrt(i_vox[0]**2+i_vox[2]**2)
        #d_arr.append(d)
        #del d
    #rad = np.percentile(d_arr,90)
    #proj_area = rad**2*pi
    #print(rad,proj_area)
    #print('Projection area calculated.')
    #print('Radius is: %f, Projection area is: %f' % (rad,proj_area))
    #print('It takes %s seconds.' % (time.time()-start_time))
    #print('--------------------------------------------------------------')
    #return proj_area

def clustering(vox_arr,origin):
    vox_out_cubes = vox_arr
    cub_slvl_ind = np.searchsorted(np.array(vox_out_cubes)[:,2],origin[2]+((i_z+1)*space),side='left')
    vox_out_lvl = vox_out_cubes[:cub_slvl_ind]
    for i_y, i_x in itertools.product(range(num_cubes_y+1),range(num_cubes_x+1)):
        origin_cube = [origin[0]+(i_x*space), origin[1]+(i_y*space), origin[2]+(i_z*space)]
        vox_in_cube, t_vox_out_cubes = get_shoots_in_cube(vox_out_lvl, origin_cube, space, space)
    #t_vox_out_cubes.extend(vox_out_cubes[cub_slvl_ind:])
        del vox_out_lvl
        vox_out_lvl = t_vox_out_cubes
        del t_vox_out_cubes
        shoots_in_cube = int(len(vox_in_cube)/shoot_coef)
        if shoots_in_cube != 0:
            vox_data = np.array(vox_in_cube)
            centroids = kmeans(vox_data, shoots_in_cube)[0]
            vox_dist_arr.extend(centroids)
    # print(len(vox_out_lvl))
    t_vox_arr = vox_out_cubes[cub_slvl_ind:]
    del vox_out_cubes
    vox_out_cubes = t_vox_arr
    del t_vox_arr


##def distribute_needles(shoot_num, vox_arr, space, shoot_distr_path, max_veg, env_cube_size):
#def distribute_needles(vox_arr, m_tree, m_setup):
    #"""
    #Make a file with information about transformation of the needle shoot model. The procedure use a cluster method
    #kmean to determine the best position for the shoot in each cube.
    #@param shoot_num: Number of shoots in whole tree
    #@param vox_arr: Array of voxels in whole tree
    #@param space: distance for separation of the tree into smaller cubes, where is calculated the coordinates for shoot
                  #position.
    #@param shoot_distr_path: Path to the file where we save the coordinates of all the shoots and angle for their
                  #rotation.
    #@param max_veg: maximum of the z coordinate in whole tree. It is needed for the calculation of the angle
                  #for transformation fo the needle shoots.
    #@param env_cube_size: Size of cube, where suppose to be calculated the envelop.
    #@return: nothing. Only create the files.
    #"""
    #print(Back.BLUE+'Finding all the clusters for shoot distribution:'+Style.RESET_ALL)
    #start_time = time.time()
    #shoot_coef = len(vox_arr)/m_tree.shoot_number
    #origin = np.amin(vox_arr, axis=0)
    #end = np.amax(vox_arr, axis=0)
    #space = m_tree.cluster_cs
    #num_cubes_x = int((end[0] - origin[0])/space)
    #num_cubes_y = int((end[1] - origin[1])/space)
    #num_cubes_z = int((end[2] - origin[2])/space)
    #vox_arr = sorted(vox_arr, key=lambda x: x[2])
    ##vox_out_cubes = vox_arr
    #vox_dist_arr = []
    ##for i_z, i_y, i_x in itertools.product(range(num_cubes_z+1),range(num_cubes_y+1),range(num_cubes_x+1)):
    #inputs = tqdm(range(num_cubes_z+1))
    
    
    ## orginaly commented from here 
    #for i_z in tqdm(range(num_cubes_z+1)):
        #cub_slvl_ind = np.searchsorted(np.array(vox_out_cubes)[:,2],origin[2]+((i_z+1)*space),side='left') # for quicker selection of the z-level cubes, it was sorted
        #vox_out_lvl = vox_out_cubes[:cub_slvl_ind]
        #for i_y, i_x in itertools.product(range(num_cubes_y+1),range(num_cubes_x+1)):
            #origin_cube = [origin[0]+(i_x*space), origin[1]+(i_y*space), origin[2]+(i_z*space)]
            #vox_in_cube, t_vox_out_cubes = get_shoots_in_cube(vox_out_lvl, origin_cube, space, space)
        ##t_vox_out_cubes.extend(vox_out_cubes[cub_slvl_ind:])
            #del vox_out_lvl
            #vox_out_lvl = t_vox_out_cubes
            #del t_vox_out_cubes
            #shoots_in_cube = int(len(vox_in_cube)/shoot_coef)
            #if shoots_in_cube != 0:
                #vox_data = np.array(vox_in_cube)
                #centroids = kmeans(vox_data, shoots_in_cube)[0]
                #vox_dist_arr.extend(centroids)
        ## print(len(vox_out_lvl))
        #t_vox_arr = vox_out_cubes[cub_slvl_ind:]
        #del vox_out_cubes
        #vox_out_cubes = t_vox_arr
        #del t_vox_arr
    ## orginaly commented to here


    #print('The clusters found.')
    #print('It takes %s seconds.' % (time.time()-start_time))
    #print('--------------------------------------------------------------')
    #print(Back.BLUE+'Distributing the shoots into the tree crown and separate them into two groups:'+Style.RESET_ALL)
    #start_time = time.time()
    #env_arr, d = find_envelop(vox_dist_arr, origin, end, space, m_tree.env_cs)
    #border_arr, inside_arr = split_needles(vox_dist_arr, env_arr, m_tree.env_cs, d, m_tree.max_veg)
    #t_file_edge_name = m_setup.cur_pos_path + '.csv'
    #t_file_edge = open(t_file_edge_name, 'w')
    #t_file_edge_csv = csv.writer(t_file_edge, delimiter=' ')
    #for i_vox in tqdm(border_arr):
        #angle = get_shoot_angle(i_vox[1], m_tree.max_veg)
        #t_line = [i_vox[0], i_vox[1], i_vox[2], angle]
        #t_file_edge_csv.writerow(t_line)
        #del t_line
    #t_file_in_name = m_setup.cur_pos_path + '.csv'
    #t_file_in = open(t_file_in_name, 'w')
    #t_file_in_csv = csv.writer(t_file_in, delimiter=' ')
    #for i_vox in tqdm(inside_arr):
        #angle = get_shoot_angle(i_vox[1], m_tree.max_veg)
        #t_line = [i_vox[0], i_vox[1], i_vox[2], angle]
        #t_file_in_csv.writerow(t_line)
        #del t_line
    #t_file_edge.close()
    #t_file_in.close()
    #print('Distribution files created.')
    #print('It takes %s seconds.' % (time.time()-start_time))
    #print('--------------------------------------------------------------')


#def get_shoots_in_cube(vox_arr, origin, size, height):
    #"""
    #Find the voxels lying in the cube.
    #@param vox_arr: array of voxels are sought the voxels only in current cube
    #@param origin: origin corners of the cube
    #@param size: size of the cube edge in x and y dimension
    #@param height: z dimension of the cube
    #@return: list of voxels in the cube and list of voxels out of the cube
    #"""
    #vox_in = []
    #vox_out = []
    #for i_vox in vox_arr:
        #if (origin[0] <= i_vox[0] < origin[0]+size) and (origin[1] <= i_vox[1] < origin[1]+height) and (origin[2] <= i_vox[2] < origin[2]+size):
            #vox_in.append(i_vox)
        #else:
            #vox_out.append(i_vox)
    #return vox_in, vox_out


#def load_shoot_voxels(shoot_file):
    #"""
    #Load voxels from shoot file. Only voxels not faces.
    #@param shoot_file: Obj file with shoot voxel coordinates.
    #@return: voxel array with the needle shoot
    #"""
    #vox_arr = []
    #for i_row in shoot_file:
        #if i_row[0] == 'v':
            #vox_arr.append([float(i_row[1]), float(i_row[2]), float(i_row[3])])
    #return vox_arr


#def transform(vox_arr, loc, angle):
    #"""
    #Transform voxels of shoot in to new coordinates after translation and rotation.
    #@param vox_arr: Array of shoot voxels to transformation.
    #@param loc: New location of the shoot.
    #@param angle: Angle for rotation of the shoot.
    #@return: New set of voxel coordinates for shoot.
    #"""

    #alpha = atan(abs(loc[2])/abs(loc[0]))
    #if loc[0] > 0 and loc[2] < 0:
        #alpha = - alpha
    #elif loc[0] < 0 and loc[2] > 0:
        #alpha = pi - alpha
    #elif loc[0] < 0 and loc[2] < 0:
        #alpha = -pi + alpha
    #else:
        #pass
    #beta = uniform(-pi/4, pi/4)
    #gama = angle
    #psi = alpha+beta+pi
    #t_vox_arr = []
    #for i_vox in vox_arr:
        #x_rot_1 = (i_vox[0]*cos(gama)-i_vox[1]*sin(gama))
        #y_rot_1 = i_vox[2]
        #z_rot_1 = (i_vox[0]*sin(gama)+i_vox[1]*cos(gama))
        #x_rot = (cos(psi)*x_rot_1)-(sin(psi)*y_rot_1)
        #y_rot = (sin(psi)*x_rot_1)+(cos(psi)*y_rot_1)
        #z_rot = z_rot_1
        #x_tra = x_rot + loc[0]
        #y_tra = y_rot + loc[2]
        #z_tra = z_rot + loc[1]
        #t_vox = [x_tra, z_tra, y_tra]
        #t_vox_arr.append(t_vox)
    #return t_vox_arr


#def get_shoot_angle(z_coo, tree_height):
    #"""
    #Define the angle depending on height in the tree.
    #@param z_coo: Z coordinates of the shoot location
    #@param tree_height: Tree height
    #@return: angle of the shoot
    #"""
    #if z_coo >= tree_height-2:
        #angle = (35 + uniform(-5, 12)) * pi/180
    #elif tree_height-2 > z_coo >= tree_height-3:
        #angle = (5 + uniform(-5, 15)) * pi/180
    #elif tree_height-3 > z_coo >= tree_height-4:
        #angle = (-15 + uniform(-5, 30)) * pi/180
    #elif tree_height-4 > z_coo >= tree_height-5:
        #angle = (-35 + uniform(-10, 40)) * pi/180
    #elif tree_height-5 > z_coo >= tree_height-6:
        #angle = (-45 + uniform(-5, 40)) * pi/180
    #elif tree_height-6 > z_coo >= tree_height-7:
        #angle = (-25 + uniform(-15, 20)) * pi/180
    #elif tree_height-7 > z_coo:
        #angle = (-35 + uniform(-15, 15)) * pi/180
    #angle = pi/2 - angle
    #return angle


#def find_envelop(vox_arr, origin, end, space, start_cube_size):
    #"""
    #Find the envelop of the whole tree. It is needed to determine the 20% of the needle shoots lying on the edge
    #of the tree as a youngest shoots.
    #@param vox_arr: The array of the position of the shoots. It could be whole point cloud, but there the algorithm will
                #take more time.
    #@param origin: the origin of the vox_arr (the minimal value of all voxels in all the three dimensions)
    #@param end: the end of the vox_arr (the maximal value of all voxels in all the three dimensions)
    #@param space: The size of the cube, where we sought the clusters for shoot distribution.
    #@param start_cube_size:
    #@return: List of voxels representing the envelop of the tree, size of the finer cubes in envelop
    #"""
    #print(Fore.CYAN+'Computing the envelop:'+Style.RESET_ALL)
    #start_time = time.time()
    #cube_size = start_cube_size
    #num_l_cubes = ceil(cube_size/space)
    #d = cube_size/num_l_cubes
    #num_cubes_x = int((end[0] - origin[0])/cube_size)+1
    #num_cubes_y = int((end[1] - origin[1])/cube_size)+1
    #num_cubes_z = int((end[2] - origin[2])/cube_size)+1
    #env_arr = []
    #for i_x,i_y,i_z in tqdm(itertools.product(range(num_cubes_x),range(num_cubes_y),range(num_cubes_z))):
        #origin_cube = [origin[0]+(i_x*cube_size), origin[1]+(i_y*cube_size), origin[2]+(i_z*cube_size)]
        #vox_in_cube = get_shoots_in_cube(vox_arr, origin_cube, cube_size, cube_size)[0]
        #if len(vox_in_cube) != 0:
            #cube_bi = get_border_index(vox_arr, origin_cube, cube_size)
            #if cube_bi > 0:
                #env_arr.append(origin_cube)
    #t_env_arr = []
    ##print_vox_to_txt(env_arr, 'data/env_rougher_arr_test')
    #vox_out = env_arr
    #height = origin[1]
    #while len(vox_out) > 0:
        #vox_in_height, vox_out = get_z_voxels(vox_out, height, 0)
        #height += cube_size
        #if len(vox_in_height) > 0:
            #t_env_arr.extend(find_finer_edge(vox_in_height, cube_size, d))
    
    ##print_vox_to_txt(t_env_arr, 'data/env_arr_test')
    ##print_vox_to_txt(vox_arr, 'data/distr_arr_test')
    #print('Envelop found.')
    #print('It takes %s seconds.' % (time.time()-start_time))
    #print('--------------------------------------------------------------')
    #return t_env_arr, d


#def get_border_index(vox_arr, origin, size):
    #"""
    #Find index representing how much cubes around current one is empty. It was searched all 26 cubes around current one.
    #@param vox_arr: all the voxels, where we want to find the neighbors
    #@param origin: origin of the central cube, around which are searching neighbors
    #@param size: size of the cubes
    #@return: border index, which says how much cubes around is empty
    #"""
    #origins_shift = [[-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0], [0, 0, -1], [0, 0, 1]]
    #origins_shift.extend([[-1, -1, 0], [1, -1, 0], [-1, 1, 0], [1, 1, 0]])
    #origins_shift.extend([[-1, 0, -1], [1, 0, -1], [-1, 0, 1], [1, 0, 1]])
    #origins_shift.extend([[0, -1, -1], [0, 1, -1], [0, -1, 1], [0, 1, 1]])
    #origins_shift.extend([[-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1]])
    #origins_shift.extend([[1, -1, -1], [1, -1, 1], [1, 1, -1], [1, 1, 1]])
    #cube_border_index = 0
    #for i_shift in origins_shift:
        #origin_cube = [origin[0]+i_shift[0]*size, origin[1]+i_shift[1]*size, origin[2]+i_shift[2]*size]
        #vox_in_cube = get_shoots_in_cube(vox_arr, origin_cube, size, size)[0]
        #num_vox_1 = len(vox_in_cube)
        #del vox_in_cube, origin_cube
        #if num_vox_1 == 0:
            #cube_border_index += 1
    #return cube_border_index


#def get_z_voxels(vox_arr, height, range_h):
    #"""
    #Find the voxels in the same height. It works only on voxels from envelop where is exact levels of height.
    #@param vox_arr: Array of voxels, where we want to find the voxels at the same height level
    #@param height: The height where we want to find the voxels.
    #@param range_h:
    #@return: List of voxels where is in the same height and the list of the rest voxels
    #"""
    #vox_in = []
    #vox_out = []
    #for i_vox in vox_arr:
        ## print('i_vox[1]: ',round(i_vox[1], 2), 'height: ',round(height, 2),  'diff: ', round(i_vox[1], 2) - round(height, 2), range_h)
        #if 0 <= (round(i_vox[1], 3) - round(height, 3)) <= range_h:
            #vox_in.append(i_vox)
        #else:
            #vox_out.append(i_vox)
    #return vox_in, vox_out


#def find_finer_edge(vox_arr, cube_size, d):
    #"""
    #Find finer edge. It works on height level. It change only x and y coordinates. NOT z.
    #@param vox_arr: Array of voxels in the envelop in the same height.
    #@param cube_size: size of the cube in envelop scale
    #@param d: the size which we want for the finer envelop, it should be close to the size of cube for the finding
                #the clusters by distribution of the needle shoots.
    #@return: list of the voxels in fines distribution
    #"""
    #if len(vox_arr) > 6:
        #t_vox_arr = fill_envelop(vox_arr, cube_size)
    #else:
        #t_vox_arr = vox_arr
    #z_coo = vox_arr[0][1]
    #num_l_cubes = int(cube_size/d)
    #new_vox_arr_0 = []
    #for i_vox in t_vox_arr:
        #for i in range(num_l_cubes):
            #x_coo = i_vox[0] + i*d
            #y_coo = i_vox[2]
            #new_vox_arr_0.append([x_coo, z_coo, y_coo])
            #del x_coo, y_coo
    #new_vox_arr_1 = []
    #for i_vox in new_vox_arr_0:
        #for i in range(num_l_cubes):
            #x_coo = i_vox[0]
            #y_coo = i_vox[2] + i*d
            #new_vox_arr_1.append([x_coo, z_coo, y_coo])
            #del x_coo, y_coo
    #del new_vox_arr_0
    #new_vox_arr_2 = reduce_envelop(new_vox_arr_1, d)
    #return new_vox_arr_2


#def reduce_envelop(vox_arr, space):
    #"""
    #Reduce the number of voxels in the envelop after get finer envelop. It is need to reduce the envelop only on
    #one layer on edge. It is all done only on one height level.
    #@param vox_arr: Array of voxels in one height level.
    #@param space: the size of the finer cubes
    #@return: array of the reduced number of voxels from envelop in one height level
    #"""
    #red_vox_arr = []
    #min_coo = np.amin(vox_arr, axis=0)
    #max_coo = np.amax(vox_arr, axis=0)
    #num_x = int((max_coo[0]-min_coo[0])/space)+1
    #num_y = int((max_coo[2]-min_coo[2])/space)+1
    #for i_x in range(num_x):
        #x_coo = min_coo[0] + (i_x*space)
        #t_vox_arr = []
        #for i_vox in vox_arr:
            #if round(i_vox[0], 3) == round(x_coo, 3):
                #t_vox_arr.append(i_vox)
        #if t_vox_arr:
            #t_vox_arr.sort()
            #red_vox_arr.extend([t_vox_arr[0], t_vox_arr[-1]])
            #del t_vox_arr
    #for i_y in range(num_y):
        #y_coo = min_coo[2] + (i_y*space)
        #t_vox_arr = []
        #for i_vox in vox_arr:
            #if round(i_vox[2], 3) == round(y_coo, 3):
                #t_vox_arr.append(i_vox)
        #if t_vox_arr:
            #t_vox_arr.sort()
            #red_vox_arr.extend([t_vox_arr[0], t_vox_arr[-1]])
            #del t_vox_arr
    #return red_vox_arr


#def fill_envelop(vox_arr, cube_size):
    #"""
    #Fill the gaps in the envelop, it is needed for the find finer edge and reducing of the envelop after that. It is
    #done in one height level.
    #@param vox_arr: Array of the voxels in one height for the filling the gaps
    #@param cube_size: size of the cube. It suppose to be the size before fining the edges
    #@return: array of the voxels with added filled voxels
    #"""
    #t_vox_arr_1 = []
    #z_coo = vox_arr[0][1]
    #min_coo = np.amin(vox_arr, axis=0)
    #max_coo = np.amax(vox_arr, axis=0)
    #num_x = int((max_coo[0] - min_coo[0])/cube_size)+1
    #num_y = int((max_coo[2] - min_coo[2])/cube_size)+1
    #for i_x in range(num_x):
        #x_coo = min_coo[0]+(i_x*cube_size)
        #t_y_arr = []
        #for i_vox in vox_arr:
            #if round(i_vox[0], 3) == round(x_coo, 3):
                #t_y_arr.append(i_vox[2])
        #if t_y_arr:
            #t_y_arr.sort()
            #i_y_arr_ran = int((t_y_arr[-1] - t_y_arr[0])/cube_size)+1
            #for i_y in range(len(t_y_arr)):
                #t_vox_arr_1.append([x_coo, z_coo, t_y_arr[i_y]])
                #if len(t_y_arr) != i_y_arr_ran and i_y > 0:
                    #dif = t_y_arr[i_y] - t_y_arr[i_y-1]
                    #if round(dif, 3) > round(cube_size, 3):
                        #num_gaps = int(dif/cube_size)
                        #for d_i in range(num_gaps):
                            #t_vox_arr_1.append([x_coo, z_coo, t_y_arr[i_y-1]+(cube_size*d_i)])
        #del t_y_arr, x_coo
    #t_vox_arr_2 = []
    #for i_y in range(num_y):
        #y_coo = min_coo[2]+(i_y*cube_size)
        #t_x_arr = []
        #for i_vox in t_vox_arr_1:
            #if round(i_vox[2], 3) == round(y_coo, 3):
                #t_x_arr.append(i_vox[0])
        #if t_x_arr:
            #t_x_arr.sort()
            #i_x_arr_ran = int((t_x_arr[-1] - t_x_arr[0])/cube_size)+1
            #for i_x in range(len(t_x_arr)):
                #t_vox_arr_2.append([t_x_arr[i_x], z_coo, y_coo])
                #if len(t_x_arr) != i_x_arr_ran and i_x > 0:
                    #dif = t_x_arr[i_x] - t_x_arr[i_x-1]
                    #if round(dif, 3) > round(cube_size, 3):
                        #num_gaps = int(dif/cube_size)
                        #for d_i in range(num_gaps):
                            #t_vox_arr_2.append([t_x_arr[i_x-1]+(cube_size*d_i), z_coo, y_coo])
        #del t_x_arr, y_coo
    #return t_vox_arr_2


#def split_needles(vox_arr, env_arr, cube_size, d, tree_height):
    #"""
    #Split voxels of the needles in to two groups. One on the edge of the tree represent the youngest needles and
    #second in the center of the tree (rest of the needles) represent the older needles.
    #@param vox_arr: Array of the all voxels
    #@param env_arr: Array of the tree edge voxels
    #@param cube_size: Size of the cube, which was used for finding the envelop
    #@param d: the size of the smaller cubes in finer envelop.
    #@param tree_height: Height of the tree. The maximum z coordinate.
    #@return: array of the voxels on the edge of the tree (the young needles), array of the voxels in the center
            #of the tree (the older needles)
    #"""
    #print(Fore.CYAN+'Splitting shoots into two groups:'+Style.RESET_ALL)
    #start_time = time.time()
    #vox_in_arr = []
    #vox_edge_arr = []
    #vox_env_out = env_arr
    #origin = np.amin(vox_env_out, axis=0)
    #height = origin[1]
    #vox_out = vox_arr
    #while len(vox_env_out) > 0:
        #per = 0
        #vox_env_in_height, vox_env_out = get_z_voxels(vox_env_out, height, 0)
        #vox_in_height, vox_out = get_z_voxels(vox_out, height, cube_size)
        #if len(vox_env_in_height) > 0 and len(vox_in_height) > 0:
            #per_lim = get_per(height, tree_height)
            #edge_cubes = vox_env_in_height
            #while per < per_lim:
                #vox_in_cubes = []
                #vox_rest = vox_in_height
                #for i_cube in edge_cubes:
                    #t_vox_in, vox_rest = get_shoots_in_cube(vox_rest, i_cube, d, cube_size)
                    #vox_in_cubes.extend(t_vox_in)
                    #del t_vox_in
                #per = len(vox_in_cubes)/len(vox_in_height)
                #if per < per_lim:
                    #t_env_arr = []
                    #t_env_arr.extend(get_more_space(vox_env_in_height, d))
                    #edge_cubes.extend(t_env_arr)
                ## if len(t_env_arr) > len():  # it is only a temporarily solution it is need to be solved differently
                ##     break
            #vox_edge_arr.extend(vox_in_cubes)
            #vox_in_arr.extend(vox_rest)
        #height += cube_size
    #print('Shoots split.')
    #print('It takes %s seconds.' % (time.time()-start_time))
    #print('--------------------------------------------------------------')
    #return vox_edge_arr, vox_in_arr


#def get_per(z_coo, tree_height):
    #"""
    #Get the percent of the young needles for the current height level on the tree.
    #@param z_coo: Z coordinates corresponding to height level in the tree.
    #@param tree_height: The height of the tree.
    #@return: The percent of the young needle in the current height level
    #"""
    #dis = 0.8
    #sd = uniform(-0.05, 0.05)
    #if z_coo >= tree_height-dis:
        #per = (0.66 + sd)
    #elif tree_height-dis > z_coo >= tree_height-(dis*2):
        #per = (0.68 + sd)
    #elif tree_height-(dis*2) > z_coo >= tree_height-(dis*3):
        #per = (0.48 + sd)
    #elif tree_height-(dis*3) > z_coo >= tree_height-(dis*4):
        #per = (0.31 + sd)
    #elif tree_height-(dis*4) > z_coo >= tree_height-(dis*5):
        #per = (0.26 + sd)
    #elif tree_height-(dis*5) > z_coo >= tree_height-(dis*6):
        #per = (0.24 + sd)
    #elif tree_height-(dis*6) > z_coo >= tree_height-(dis*7):
        #per = (0.18 + sd)
    #elif tree_height-(dis*7) > z_coo >= tree_height-(dis*8):
        #per = (0.10 + sd)
    #elif tree_height-(dis*8) > z_coo >= tree_height-(dis*9):
        #per = (0.07 + sd)
    #elif tree_height-(dis*9) > z_coo:
        #per = 0.05
    #return per


#def get_more_space(vox_arr, cube_size):
    #"""
    #Find the next level from the edge of the tree. Deeper in the tree. Only on the one height level.
    #@param vox_arr: array with voxels from envelop on the current height level
    #@param cube_size: Size of the cube, the smaller one from envelop finding.
    #@return: Array of the voxels lying next to the envelop voxels closer to the center of teh tree.
    #"""
    #min_coo = np.amin(vox_arr, axis=0)
    #max_coo = np.amax(vox_arr, axis=0)
    #num_x = int((max_coo[0] - min_coo[0])/cube_size)+1
    #num_y = int((max_coo[2] - min_coo[2])/cube_size)+1
    #t_new_vox_arr_1 = []
    #for i_x in range(num_x):
        #x_coo = min_coo[0] + (i_x*cube_size)
        #for i_vox in vox_arr:
            #if round(i_vox[0], 3) == round(x_coo, 3):
                #if x_coo > 0 and (x_coo - cube_size) > 0:
                    #t_x_coo = x_coo - cube_size
                #elif x_coo < 0 and (x_coo + cube_size) < 0:
                    #t_x_coo = x_coo + cube_size
                #elif round(x_coo, 1) == 0:
                    #t_x_coo = x_coo
                #try:
                    #t_new_vox_arr_1.append([t_x_coo, i_vox[1], i_vox[2]])
                    #del t_x_coo
                #except UnboundLocalError:
                    #pass
    #t_new_vox_arr_2 = []
    #for i_y in range(num_y):
        #y_coo = min_coo[2] + (i_y*cube_size)
        #for i_vox in t_new_vox_arr_1:
            #if round(i_vox[2], 3) == round(y_coo, 3):
                #if y_coo > 0 and (y_coo - cube_size) > 0:
                    #t_y_coo = y_coo - cube_size
                #elif y_coo < 0 and (y_coo + cube_size) < 0:
                    #t_y_coo = y_coo + cube_size
                #elif round(y_coo, 1) == 0:
                    #t_y_coo = y_coo
                #try:
                    #t_new_vox_arr_2.append([i_vox[0], i_vox[1], t_y_coo])
                    #del t_y_coo
                #except UnboundLocalError:
                    #pass
    #return t_new_vox_arr_2


#def create_shoot_info_file(m_setup, m_tree):
#def create_shoot_info_file(veg_path, tree_name, shoot_distr_path, space, shoot_area, LAI_value, max_veg, env_cube_size):
    """
    Procedure for prepare and create a file with distribution of the needle shoot.
    @param veg_path: Path to the folder with the data of the three
    @param tree_name: Name of the tree
    @param shoot_distr_path: Path to the shoot distribution file
    @param space: Size of the cube to separated the whole tree in cells
    @param shoot_area: Area of the whole shoot without the twig
    @param LAI_value: Value of the LAI which we want to realize
    @param max_veg:
    @param env_cube_size:
    @return: nothing. Only create and prepare a distribution file
    """
    #voxel_list = load_voxels(m_setup.source_dir, m_tree.name)
    #projection_area = find_projection_area(voxel_list)
    #shoot_number = (2*m_tree.LAI*projection_area)/m_tree.s_area
    #distribute_needles(voxel_list, m_tree, m_setup)


def create_shoot_obj_file(shoot_obj_path, shoot_distr_path, shoot_path):
    """
    Create obj file with needle shoots.
    @param shoot_obj_path: Path to the obj file with needle shoots
    @param shoot_distr_path: Path to the file with distribution info about shoots location
    @param shoot_path: Path to the file with one shoot.
    @return: nothing. Only create a obj file with shoots
    """
    start_time = time.time()
    obj_file = open(shoot_obj_path, 'w')
    obj_csv_file = csv.writer(obj_file, delimiter=' ')
    distr_file = open(shoot_distr_path, 'r')
    distr_csv_file = csv.reader(distr_file, delimiter=' ')
    shoot_file = open(shoot_path, 'r')
    shoot_csv_file = csv.reader(shoot_file, delimiter=' ')
    shoot_vox_arr = load_shoot_voxels(shoot_csv_file)
    shoot_file.close()
    shoot_file = open(shoot_path, 'r')
    shoot_csv_file = csv.reader(shoot_file, delimiter=' ')
    shoot_vox_num = len(shoot_vox_arr)
    tt_line = ['#', 'Some', 'description', 'comment']
    obj_csv_file.writerow(tt_line)
    del tt_line
    tt_line = ['#', 'Some', 'other', 'description', 'comment']
    obj_csv_file.writerow(tt_line)
    del tt_line
    tt_line = ['#']
    obj_csv_file.writerow(tt_line)
    del tt_line
    tt_line = ['g', 'Tree', 'with', 'shoots']
    obj_csv_file.writerow(tt_line)
    del tt_line
    ind_shoot = 0
    for i_row in distr_csv_file:
        trans_info = [float(i_row[0]), float(i_row[1]), float(i_row[2])]
        rot_info = float(i_row[-1])
        trans_vox_arr = transform(shoot_vox_arr, trans_info, rot_info)
        ind_vox = 0
        for i_row_shoot in shoot_csv_file:
            if i_row_shoot[0] == 'v':
                t_line = ['v']+trans_vox_arr[ind_vox]
                ind_vox += 1
            elif i_row_shoot[0] == 'f':
                vox_1 = str(int(float(i_row_shoot[1])+ind_shoot*shoot_vox_num))
                vox_2 = str(int(float(i_row_shoot[2])+ind_shoot*shoot_vox_num))
                vox_3 = str(int(float(i_row_shoot[3])+ind_shoot*shoot_vox_num))
                t_line = ['f'] + [vox_1, vox_2, vox_3]
            elif i_row_shoot[0] == 'g':
                t_line = i_row_shoot
            # else:
            #     if i_row_shoot[0] == '#':
            #         pass
            #     else:
            #         t_line = i_row_shoot
            try:
                obj_csv_file.writerow(t_line)
                del t_line
            except UnboundLocalError:
                pass
        shoot_file.close()
        shoot_file = open(shoot_path, 'r')
        shoot_csv_file = csv.reader(shoot_file, delimiter=' ')
        ind_shoot += 1
    obj_file.close()
    distr_file.close()
    shoot_file.close()
    print('obj file created.')
    print('It takes %s seconds.' % (time.time()-start_time))
    print('--------------------------------------------------------------')

def print_vox_to_txt(vox_arr, file_name):
    txt_file = open(file_name + '.txt', 'w')
    for i_vox in vox_arr:
        t_line = str(i_vox[0]) + ' ' + str(i_vox[1]) + ' ' + str(i_vox[2]) + '\n'
        txt_file.write(t_line)
