# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 11:11:37 2022

Custom function used to select data for analysis.

@author: Administrator
"""

"""Select Data to import"""

# Tkinter utilites for GUI interaction
import tkinter as tk
from tkinter import filedialog as fd # Used to pull files via gui
import scipy.io as sio # To read in .mat file types
import numpy as np

def select_data(_dir_DATA):
    
    """
    Function that prompts the user to browse directories and select the 
    target RCS data file. Data files are type .mat. They are created using
    matlab code provided by the AFIT EENG 627 course. This code uses a binary 
    read-funciton written by the radar developer that is written in matlab. 
    
    Input:
        None
        
    Output:
        None
        
    """
    
    # identify data to load
    root = tk.Tk()
    # root.withdraw()
    root.lift()
    path = fd.askopenfilename(initialdir=_dir_DATA)
    root.destroy()

    # Pull the rsr object from matlab
    data = sio.loadmat(path, mdict=None, appendmat=True)
    keys = list(data.keys())
    data = data[keys[-1]]
    data = data[0,0]
    
    # Data to dictionary
    rcs = {}
    rcs.update({'frq' : np.asarray(data[0])[0]})
    rcs.update({'ph' : np.asarray(data[1])[0]})
    rcs.update({'th' : data[2]})
    rcs.update({'tt' : np.asarray(data[12])})
    rcs.update({'pp' : np.asarray(data[13])})
    rcs.update({'tp': data[14]})
    rcs.update({'pt' : data[15]})
    rcs.update({'header' : data[16]})
    
    # Process probability info
    mean_labels = [['fm_tt', 'fm_pp'],
                   ['am_tt', 'am_pp']]
    
    var_labels = [['fv_tt', 'fv_pp'],
                  ['av_tt', 'av_pp']]
    labels = {'mean':mean_labels, 'var':var_labels}
    for key in labels.keys():
        l = labels[key]
        
        if key == 'mean':
            "Mean response over all freqs per angle"
            rcs.update( {l[0][0]:np.mean(rcs['tt'], axis=0)} )
            rcs.update( {l[0][1]:np.mean(rcs['pp'], axis=0)} )
            "Mean response over all angles per freq"
            rcs.update( {l[1][0]:np.mean(rcs['tt'], axis=1)} )
            rcs.update( {l[1][1]:np.mean(rcs['pp'], axis=1)} )
            
        elif key == 'var':
            # Mean over freqs
            rcs.update( {l[0][0]:np.var(rcs['tt'], axis=0)} )
            rcs.update( {l[0][1]:np.var(rcs['pp'], axis=0)} )
            # Mean over angle
            rcs.update( {l[1][0]:np.var(rcs['tt'], axis=1)} )
            rcs.update( {l[1][1]:np.var(rcs['pp'], axis=1)} )
    # End prob extraction

    return rcs







