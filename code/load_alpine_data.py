# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 12:40:25 2022

- RCS data processing from freq domain to time

@author: Administrator
"""

# %% Import Statements
#import tensorflow as tf
#import pickle as pkl
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, time, math
from datetime import datetime


# Pull custom functions
from Process_IFFT import process_ifft
from Select_Data import select_data
from Process_FFE import process_ffe

# %% Constants

# Enable ANSI colors
os.system('color')
# Define colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class usr_msg:
    warno = 'warno'
    prompt = 'prompt'
    notice = 'notice'
    fail = 'fail'
    
NYQUIST = 2  


#%% Functions

"""User message system -- colros used to denote message type"""
def user_message(_text, _type):

    if _type == 'warno':
        print(bcolors.WARNING + _text + bcolors.ENDC + '\n', flush=True)
    elif _type == 'prompt':
        print(bcolors.OKGREEN + _text + bcolors.ENDC + '\n', flush=True)
    elif _type == 'notice':
        print(bcolors.OKBLUE + _text + bcolors.ENDC + '\n', flush=True)
    elif _type == 'fail':
        print(bcolors.FAIL + _text + bcolors.ENDC + '\n', flush=True)

"""Create directories"""
def build_directories():
    
    """
    Builds directories variabels that are used to find data
    
    Input:
        Empty
    Output:
        ROOT = root directory for the program
        dir_DATA = data directory
        dir_FIG = figures directory
        dir_MWIR = mwir data directory
        dir_LWIR = lwir data directory
    """
    user_message('Building Directories' , usr_msg.notice)
    
    PATH = os.path.dirname(__file__)
    os.chdir(PATH)
    os.chdir('..')
    _ROOT = os.getcwd()
    _dir_DATA = os.path.join(_ROOT, 'data')
    _dir_FIG = os.path.join(_ROOT, 'figures')
    
    return(_ROOT, _dir_DATA, _dir_FIG)
# End directory builder

"""Plotter"""
def plotter(_fig_num, _data, _labels):
    
    plt.rcParams.update({'font.size': 22})
    
    plt.figure(_fig_num)
    plt.plot(_data[0], _data[1])
    plt.title(_labels[0])
    plt.ylabel(_labels[1])
    plt.xlabel(_labels[2])
    plt.grid(which='both', axis='both', linestyle=':')
    plt.legend()

"""Extract Data from an RCS struct"""
def extract_data(_rcs_data, _f, _a, _pol):
    
    """Extract the data from an AFIT RCS struct over a certain band of 
    frequencies, azimuthal angles, or polarizations
    
    Inputs:
            _rcs_data:  input rcs data struct
            _f: requested frequeny, or frequency range. Expects np array
            _a:  requested angles
            _pol:  requested polarizations
    """
    
    # Test instances for type -- set to array if needed
    args =[_f, _a, _pol]
    for i, v in enumerate(args):
        if ~isinstance(v, np.ndarray):
            args[i] = np.array(v)
    
    # Instantiate new instance
    new_struct = rcs_data()
    _frq = _rcs_data.frq
    _ph = _rcs_data.ph
    _th = _rcs_data.th
    _tt = _rcs_data.tt
    _pp = _rcs_data.pp
    _tp = _rcs_data.tp
    _pt = _rcs_data.pt
    
    args = [_tt, _pp, _tp, _pt]
    
    # Parse input angles
    nA = len(_a)
    if nA!= 0:
        if nA > 2:
            print("Angle range too large. Pick a min and max only. ")
            return
        elif nA == 1:
            print("Extracting angles at {0}".format(str(_a)))
            _a_idx = np.where(_frq == _f[0])
            for i, v in enumerate(args):
                args[i] = args[i][:, _a_idx]
        elif nA == 2:
            print("Extracting angles at {0} and {1}".format(str(_a[0]), str(_a[1])))
            _a_idx = [ np.where(_ph == _a[0]), np.where(_ph == _a[1]) ]
            for i, v in enumerate(args):
                args[i] = args[i][_a_idx[0]:_a_idx[1], :]
    else:
        print("No angles entered.")
        
    # Parse input frequencies
    nF = len(_f) 
    if nF != 0:
        if nF > 2:
            print("Frequencies range too large. Pick a min and max only.")
            return
        elif nF == 1:
            print("Extracting frequency at {0}.".format(str(_f)))
            _f_idx = np.where(_frq == _f[0])
            for i, v in enumerate(args):
                args[i] = args[i][_f_idx, :]
        elif nF == 2:
            print("Extracting frequencies at {0}, and {1}.".format(str(_f[0]), str(_f[1])))
            _f_idx = [ np.where(_frq == _f[0]), np.where(_frq == _f[1]) ]
            for i, v in enumerate(args):
                args[i] = args[i][_f_idx[0]:_f_idx[1], :]
    else:
        print("No frequencies entered.")
     



# %% Main loop body

if __name__ == '__main__':
    
    ROOT, dir_DATA, dir_FIG = build_directories()
    
    rcs = select_data(dir_DATA)

    rcs = process_ffe(rcs)

    # plot_polar_rcs = 'y'#input("Plot polar RCS? (at 7 GHz)")
    # if plot_polar_rcs == 'y':
    #     f_idx = np.where( rcs_data.frq == 7)[0][0]
    #     s_tt = 20*np.log10(np.abs(rcs_data.tt[f_idx, :]))
    #     s_pp = 20*np.log10(np.abs(rcs_data.pp[f_idx, :]))
    #     a = rcs_data.ph
        
    #     plt.plot(a, s_tt)
    #     plt.plot(a, s_pp)
        
    #     # fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    #     # ax.plot(a, s_tt, label='V pol')
    #     # # ax.plot(a, 20*np.log10(np.abs(s_pp)), label='H pol')
    #     # # ax.set_rmax(2)
    #     # # ax.set_rticks([0.5, 1, 1.5, 2])  # Less radial ticks
    #     # # ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
    #     # ax.grid(True)
        
    #     # ax.set_title("RCS Plot", va='bottom')
    #     # plt.show()
    
    # process_ift = 'y'#input("Process IFFT?")
    # if process_ift == 'y':
        

    
    
    
    
    
    
    
