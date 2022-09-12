# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 13:01:09 2022

@author: Administrator
"""
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
import matplotlib
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

def plot_data(m_rcs, s_rcs):
    
    """
    Function used to generate data plots for the desired rcs data
    Inputs:
        m_rcs:  measurement data rcs
        s_rcs:  simulation data rcs
    Outputs:
        plots
    """
    
    """
    Generates:
        Figure 1:  3D plots for Rcs vs F at 4 angles with real and image data
    """
    
    """Pull colors given a poly collection length -- expects 12 functions!!"""
    n_funcs = 12
    cmap = cm.magma
    idx = np.linspace(0, cmap.N, n_funcs)/cmap.N # normalize between 0 and 1
    cmap = cmap(idx)
    colors = []
    for c in cmap:
        colors.append(matplotlib.colors.rgb2hex(c))
       
    
    """Pre-process data"""
    f = s_rcs['frq']
    a = [0, 90, 180, 270]
    keys = ['0', '90', '180', '270']
    s_h = {}
    s_v = {}
    m_h = {}
    m_v = {}
    # Pull columns with the correct angle
    for i, v in enumerate(a):
        idx = (np.where(s_rcs['ph']==v)[0][0])
        
        temp = []
        # Single polarization to practice
        temp.append(list(zip(f, s_rcs['pp'][:, idx].real)))       # Pull reals
        temp.append(list(zip(f, s_rcs['pp'][:, idx].imag)))       # Pull Imag
        temp.append(list(zip(f, np.abs(s_rcs['pp'][:, idx]))))
        s_h.update( {keys[i] : temp} )
        
    """Build the figure"""
    fig = plt.figure()
    ax = plt.axes(projection='3d')
        
    """Create the Poly collection 3D Plots """
    c = np.asarray([0, 3])
    z = [1, 2, 3]
    # for k in s_h.keys():
    #     poly = PolyCollection(s_h[k], facecolors=colors[c[0]:c[-1]])
    #     poly.set_alpha(0.7)
    #     ax.add_collection3d(poly, zs=z, zdir='y')
    #     c = c+4
    #     z = z+1

    poly = PolyCollection(s_h['0'])#, facecolors=colors[c[0]:c[-1]])
    poly.set_alpha(0.7)
    ax.add_collection3d(poly, zs=z, zdir='y')

    """Set Collection locations, and adjust the plots"""
    ax.set_xlabel('Freqeuncy, [GHz]')
    ax.set_xlim3d(f[0], f[-1])
    ax.set_xticks(np.arange(f[0], f[-1], 0.5))
    ax.set_ylabel('Angle, [deg]')
    ax.set_ylim3d(1,3)
    ax.set_yticks([1, 2, 3])
    ax.set_zlabel('Magnitude, [V?]')
    # ax.set_zlim3d(-0.00005, 0.00005)
    # ax.set_zticks([-1, -0.5, 0, 0.5, 1])
    ax.grid()

    plt.show()
    
    
    
    
    
    
    
    
    