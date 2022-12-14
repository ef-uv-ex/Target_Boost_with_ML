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
    
def plot_fnorms(s_rcs, m_rcs):
    
    # Plot the normed freq response at 1 angle
    plt.figure('Normed RCS over Frequency at ph = 90')
    f = s_rcs['frq']
    s1 = s_rcs['tt'][:, 0]
    s2 = m_rcs['tt'][:, 0]
    plt.title('Normed RCS vs Frequency, \n $\phi=90^{\circ}$')
    plt.xlabel('Frequency, [GHz]')
    plt.ylabel('Normalized RCS')
    plt.plot(f, s1, label='Sim')
    plt.plot(f, s2, label='Meas')
    plt.grid(which='both', axis='both')
    # End Plot Fnorms

def plot_anorms(s_rcs, m_rcs):
    
    a = s_rcs['ph']*np.pi/180
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    fig.suptitle('Normalized RCS Bugsplat at f=10 GHz')
    ax.plot(a, s_rcs['tt'][50, :], label='Sim')
    ax.plot(a, m_rcs['tt'][50, :], label='Meas')
    ax.grid(True)
    plt.show()
    
    
def plot_calVerify(s_rcs, m_rcs, a=0, f=10, pol='tt'):
    
    plt.close('all')
    _s_rcs = s_rcs.copy()
    _m_rcs = m_rcs.copy()
    key = ['tt', 'pp', 'tp', 'pt']
    
    # Plot the frequency data as a reference
    
    """Plot the Error over Frequency"""
    calVerify = {}
    calVerify.update({'frq':_s_rcs['frq']})
    temp = np.abs(_m_rcs[pol][:, a])/np.abs(_s_rcs[pol][:, a])
    calVerify.update( {pol:20*np.log(temp)} )
    
    stats = [np.mean(calVerify[pol]), 
             np.std(calVerify[pol])
             ]
    stats = np.round_(stats, decimals=2)
    plt.figure(0)
    plt.title('Normalized RCS vs Frequency, \n Polarization='+str(pol)+', $\phi=$'+str(a))
    plt.plot(_s_rcs['frq'], _s_rcs[pol][:, a], label="Sim")
    plt.plot(_m_rcs['frq'], _m_rcs[pol][:, a], label="Meas")
    plt.grid(True)
    plt.xlabel('Frequency, [GHz]')
    plt.ylabel('Amplitude')
    
    # Plot frequency range at angle a
    plt.figure(1)
    plt.title('Normalized Calibration Error vs Frequency, \n Polarization='+str(pol)+', $\phi=$'+str(a))
    plt.plot(calVerify['frq'], calVerify[pol], label=r'$\mu=$'+str(stats[0])+'\n $\sigma=$'+str(stats[1]))
    plt.grid(True)
    plt.xlabel('Frequency, [GHz]')
    plt.ylabel('Amplitude, [dB]')
    plt.legend()
    
    """Plot the Error over Angle"""
    calVerify = {}
    calVerify.update({'ph':_s_rcs['ph']})
    temp = np.abs(_m_rcs[pol][f, :])/np.abs(_s_rcs[pol][f, :])
    calVerify.update( {pol:20*np.log(temp)} )
    
    stats = [np.mean(calVerify[pol]), 
             np.std(calVerify[pol])
             ]
    stats = np.round_(stats, decimals=2)
    plt.figure(2)
    plt.title('Normalized RCS vs Angle, \n Polarization='+str(pol)+', $f=$'+str(f)+' [GHz]')
    plt.plot(_s_rcs['ph'], _s_rcs[pol][f, :], label="Sim")
    plt.plot(_m_rcs['ph'], _m_rcs[pol][f, :], label="Meas")
    plt.grid(True)
    plt.xlabel(r'Angle, [$^{\circ}$]')
    plt.ylabel('Amplitude')
    
    # Plot frequency range at angle a
    plt.figure(3)
    plt.title('Normalized Calibration Error vs Angle, \n Polarization='+str(pol)+', f='+str(f)+' [GHz]')
    plt.plot(calVerify['ph'], calVerify[pol], label=r'$\mu=$'+str(stats[0])+'\n $\sigma=$'+str(stats[1]))
    plt.grid(True)
    plt.xlabel(r'Angle, [$^{\circ}$]')
    plt.ylabel('Amplitude, [dB]')
    plt.legend()
    
    
    