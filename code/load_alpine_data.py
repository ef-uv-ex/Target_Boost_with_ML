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
import scipy.io as sio # To read in .mat file types

# Tkinter utilites for GUI interaction
import tkinter as tk
from tkinter import filedialog as fd # Used to pull files via gui

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

# %% Data object

class capture_data():
    
    def __init__(self):
        frq = []
        ph = []
        th = []
        tt = []
        pp = []
        tp = []
        pt = []
        header = []
        

# %% Main loop body

if __name__ == '__main__':
    
    ROOT, dir_DATA, dir_FIG = build_directories()
    
    # identify data to load
    root = tk.Tk()
    # root.withdraw()
    root.lift()
    path = fd.askopenfilename(initialdir=dir_DATA)
    root.destroy()

    # Pull the rsr object from matlab
    data = sio.loadmat(path, mdict=None, appendmat=True)
    keys = list(data.keys())
    data = data[keys[-1]]
    data = data[0,0]
    
    rcs_data = capture_data()
    rcs_data.frq = np.asarray(data[0])[0]
    rcs_data.ph = np.asarray(data[1])[0]
    rcs_data.th = data[2]
    rcs_data.tt = np.asarray(data[12])
    rcs_data.pp = np.asarray(data[13])
    rcs_data.tp = data[14]
    rcs_data.pt = data[15]
    rcs_data.header = data[16]
    
    del data
    
    plot_polar_rcs = 'y'#input("Plot polar RCS? (at 7 GHz)")
    if plot_polar_rcs == 'y':
        f_idx = np.where( rcs_data.frq == 7)[0][0]
        s_tt = 20*np.log10(np.abs(rcs_data.tt[f_idx, :]))
        s_pp = 20*np.log10(np.abs(rcs_data.pp[f_idx, :]))
        a = rcs_data.ph
        
        plt.plot(a, s_tt)
        plt.plot(a, s_pp)
        
        # fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        # ax.plot(a, s_tt, label='V pol')
        # # ax.plot(a, 20*np.log10(np.abs(s_pp)), label='H pol')
        # # ax.set_rmax(2)
        # # ax.set_rticks([0.5, 1, 1.5, 2])  # Less radial ticks
        # # ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
        # ax.grid(True)
        
        # ax.set_title("RCS Plot", va='bottom')
        # plt.show()
    
    process_ift = 'y'#input("Process IFFT?")
    if process_ift == 'y':
        
        # Need to grab the first col of measurement data
        # Each row of measurement data is a measure at a freq, at that inc angle
        # Lets work with column one (0 angle) for now
        rcs_tt = np.transpose(np.asarray(rcs_data.tt[:, 0]))
        # F = np.asarray(rcs_data.tt)[:, np.where(rcs_data.frq == 7)[0][0]]
        F = np.asarray(rcs_data.frq)
        
        """Process measurement data for frequency domain plot"""
        S = 20*np.log10(np.abs(rcs_tt))
        
        fig_num = 'Frequency Domain Plot'
        plot_labels = [
            r'Amplitude vs Frequency for $\phi = 0$', 
            'Amplitude, [dB]', 
            'Frequency, [GHz]',
            ]
        plot_data = [F, S]
        plotter(fig_num, plot_data, plot_labels)
        
        
        """Process measurement data for Time Domain Conversion"""
        # Define fourier values need for the IFFT
        n_bandwidth = len(F)                    # Frequency count for collected BW
        bandwidth = (F[-1] - F[0])*1e9          # Collected BW
        frq_res = bandwidth/(n_bandwidth - 1)   # Frq step resolution
        unamb_T = 1/frq_res                     # Unambiguous total time
        T_res = 1/bandwidth                     # time resolution step
        n_pow = math.ceil(math.log(NYQUIST*(n_bandwidth-1), 2))
        n_rng_bins = int(2**(n_pow + 1 ))       # Number of bins for time domain
        
        # Time vector 
        T = np.linspace(-unamb_T/2, unamb_T/2, n_rng_bins) - unamb_T/n_rng_bins/2
        
        # Apply the inverse FFT
        A = np.fft.ifft(rcs_tt, 2**n_pow)
        A = np.concatenate((np.flip(A), A))
        
        fig_num = 'Time Domain Impulse'
        plot_labels = [
            r'Impulse vs Time for $\phi = 0$', 
            'Amplitude, [V(?)]', 
            'Time, [ns]',
            ]
        plot_data = [T*1e9, np.abs(A)]
        plotter(fig_num, plot_data, plot_labels)
    
    
    
    
    
    
    
