'''
Created on 2014. 3. 24.

>>> idx_matrix = make_adjacent_idx_matrix(4)
>>> idx_matrix = make_adjacent_idx_matrix(6)
>>> idx_matrix = make_adjacent_idx_matrix(8)
@author: drtagkim
'''
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
from landscape import *

def extend_matrix(m_00,n):
    m_01 = reflect_x(m_00) + 2**n
    m_10 = reflect_y(m_00) + 2**(n+1)
    m_11 = reflect_xy(m_00) + (2**n)*3
    upper_m = np.concatenate((m_00,m_01),axis=1)
    lower_m = np.concatenate((m_10,m_11),axis=1)
    return np.concatenate((upper_m,lower_m),axis=0)
def make_adjacent_idx_matrix(N):
    #dim = 1<<(N/2)
    #dim_n = sorted(factory_sub_idx_keys(dim))
    A = np.array([0,1,2,3],dtype=np.int64).reshape(2,2)
    for i in range(0,N,2):
        if i == 0:
            m = A
        else:
            m = extend_matrix(m,i)
    return m
def reflect_x(m):
    n = m.copy()
    for i in range(len(m)):
        n[:,i] = m[:,-1*(i+1)]
    return n
def reflect_y(m):
    n = m.copy()
    for i in range(len(m)):
        n[i,:] = m[-1*(i+1),:]
    return n
def reflect_xy(m):
    n = m.copy()
    n = reflect_y(m)
    n = reflect_x(n)
    return n
def factory_sub_idx_keys(n):
    a = []
    if n == 2:
        return [2]
    else:
        a.append(n)
        a.extend(factory_sub_idx_keys(n/2))
        return a
def test(file_name,N):
    inf = construct_influence_matrix_from_file(file_name,'x')
    fit = FitnessContributionTable(inf)
    land = Landscape(fitness_contribution_matrix = fit)
    land.compute_all_locations_id()
    values = land.standardized_fitness_value
    idx_matrix = make_adjacent_idx_matrix(N)
    Z = values[idx_matrix]
    #
    max_idxs = np.where(Z == Z.max())
    max_row = max_idxs[0][0]
    max_col = max_idxs[1][0]
    Z = np.roll(Z,N/2-max_col,axis=1)
    Z = np.roll(Z,N/2-max_row,axis=0)
    X = np.arange(1<<(N/2))
    Y = np.arange(1<<(N/2))
    X, Y = np.meshgrid(X,Y)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1)
    plt.show()
