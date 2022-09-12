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
from Extract_Data import extract_data
from Plot_Data import plot_data, plot_fnorms, plot_anorms
from Norm_RCS import norm_data

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
        print(bcolors.WARNING + _text.center(len(_text)*2).capitalize() + bcolors.ENDC + '\n', flush=True)
    elif _type == 'prompt':
        print(bcolors.OKGREEN + _text.center(len(_text)*2) + bcolors.ENDC + '\n', flush=True)
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
     



# %% Main loop body

if __name__ == '__main__':
    
    ROOT, dir_DATA, dir_FIG = build_directories()

    # _text = 'Load Mini-Arrow measurement data.'
    # user_message(_text, usr_msg.prompt)    
    # m_arrow = select_data(dir_DATA)
    # m_arrow = extract_data(m_arrow, [9.5, 10.5])
    
    # _text = 'Load Mini-Arrow simulated data.'
    # user_message(_text, usr_msg.prompt) 
    # s_arrow = select_data(dir_DATA)
    
    _text = 'Load prolate measurement data.'
    user_message(_text, usr_msg.prompt)    
    m_prolate = select_data(dir_DATA)
    
    _text = 'Load prolate simulated data.'
    user_message(_text, usr_msg.prompt) 
    s_prolate = select_data(dir_DATA)

    # Plot the aximuth cut data
    #plot_data(m_prolate, s_prolate)

    s_prolate = extract_data(s_prolate)#, _a=[0, 90, 180, 270])
    m_prolate = extract_data(m_prolate, _f=[9.5, 10.51])#, _a=[0, 90, 180, 270])
    
    s_prolate_norm_a = norm_data(s_prolate, a_flag=True)
    s_prolate_norm_f = norm_data(s_prolate, f_flag=True)
    
    m_prolate_norm_a = norm_data(m_prolate, a_flag=True)
    m_prolate_norm_f = norm_data(m_prolate, f_flag=True)
    
    plot_fnorms(s_prolate_norm_f, m_prolate_norm_f)
    plot_anorms(s_prolate_norm_a, m_prolate_norm_a)
    
    
    
    
