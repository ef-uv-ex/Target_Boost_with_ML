%% Load the data from the active data folder

clc;
clear all;
close all;

% Grab data time
format = 'yyyymmdd';
t = datestr(now, format);


% Move directory
dir_CODE = "G:\Rofrano_Thesis\Project\code";
dir_FIG = "G:\Rofrano_Thesis\Project\figures";
dir_DATA = "G:\Rofrano_Thesis\Project\data";
cd(dir_DATA);

% Figure Parameters
n_int = 128;
target_type = 'Prolate Sphere';

RCS_CLIM = [-60,20];


%% Load the FEKO data

% cd("G:\Rofrano_Thesis\Project\data\Prolate");
% tar_true = readFeko('mini_arrow_20220823.ffe')

%% Save the thing

% filename = strcat(t, '_prolate_128');
% save(filename, 'tar_cal');


%% Plot the FEKO results
% close('all')
% 
% % Plot global RCS
% plotGlobalRCS(tar_true, 'caxis',RCS_CLIM);
% plotGlobalRCS(tar_true, 'caxis',RCS_CLIM);
% 
% % Plot RCS cuts in polar format
% tar_true_7 = extractData(tar_true, 'frq', 7);
% plotRCS(tar_true_7, 'polar', 'copol', 'caxis',RCS_CLIM);
% plotRCS(tar_true_7, 'copol', 'caxis',RCS_CLIM);
% 
% filename = strcat(t, '_prolate_true');
% save(filename, 'prolate_true');


