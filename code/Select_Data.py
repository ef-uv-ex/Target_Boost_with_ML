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
    
    rcs = {}
    rcs.update({'frq' : np.asarray(data[0])[0]})
    rcs.update({'ph' : np.asarray(data[1])[0]})
    rcs.update({'th' : data[2]})
    rcs.update({'tt' : np.asarray(data[12])})
    rcs.update({'pt' : np.asarray(data[13])})
    rcs.update({'tp': data[14]})
    rcs.update({'pp' : data[15]})
    rcs.update({'header' : data[16]})

    return rcs







