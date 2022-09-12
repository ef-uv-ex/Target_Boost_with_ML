# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 12:48:03 2022

@author: Administrator
"""

"""
=============================================
Generate polygons to fill under 3D line graph
=============================================

Demonstrate how to create polygons which fill the space under a line
graph. In this example polygons are semi-transparent, creating a sort
of 'jagged stained glass' effect.
"""

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
import matplotlib
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np



# Test function
dt = 0.01
t = np.arange(0, 1+dt, dt)


"""Build the figure"""
fig = plt.figure()
ax = plt.axes(projection='3d')

"""Zip the x and y terms into a tuple for the collections plotter"""
f = lambda f: np.sin(2*np.pi*f*t)
f_tot = [f(1), f(2), f(3)]
f_array = []
# Zip creates an array of tuple pairs (t[i], f[i]) needed for the collection
for f in f_tot:
    f_array.append(list(zip(t, f)))

"""Pull Color maps from a known listing, and extract only the needed colors"""
cmap = cm.magma
idx = np.linspace(0, cmap.N, len(f_array))/cmap.N # normalize between 0 and 1
cmap = cmap(idx)
colors = []
for c in cmap:
    colors.append(matplotlib.colors.rgb2hex(c))

"""Construct the PolyCollection Object"""
poly = PolyCollection(f_array, facecolors=colors)
poly.set_alpha(0.7)


"""Set Collection locations, and adjust the plots"""
zs = [1, 2, 3]
ax.add_collection3d(poly, zs=zs, zdir='y')
ax.set_xlabel('X')
ax.set_xlim3d(0, 1)
ax.set_xticks(np.arange(0, 1.25, 0.25))
ax.set_ylabel('Y')
ax.set_ylim3d(1,3)
ax.set_yticks([1, 2, 3])
ax.set_zlabel('Z')
ax.set_zlim3d(-1, 1)
ax.set_zticks([-1, -0.5, 0, 0.5, 1])
ax.grid()

plt.show()


