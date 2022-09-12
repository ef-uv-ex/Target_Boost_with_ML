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

RCS_CLIM = [-60,20];

%% Load the FEKO data

cd("G:\Rofrano_Thesis\Project\data\Prolate"); % From main drive
tar_true = readFeko('prolate_far_field.ffe');

% Rotate negative 90 to match the radar inputs
tar_true = shiftData(tar_true, -90)

tar_true.pp = tar_true.pt
tar_true.pt = []

%% Testing the output for the correct angles

tar_true_10 = extractData(tar_true, 'frq', 10);
plotRCS(tar_true_10, 'polar', 'copol', 'caxis', RCS_CLIM);

%% Save the thing

cd("G:\Rofrano_Thesis\Project\data")
filename = strcat(t, '_prolate_ffe');
save(filename, 'tar_true');


%% Plot the FEKO results
% close('all')
% RCS_CLIM = [-60,20];
% 
% % Plot global RCS
% plotGlobalRCS(tar_true);
% plotGlobalRCS(tar_true);
% 
% % Plot RCS cuts in polar format
% tar_true_10 = extractData(tar_true, 'frq', 10);
% plotRCS(tar_true_10, 'polar', 'copol');
% plotRCS(tar_true_10, 'copol');
% 
% % filename = strcat(t, '_prolate_true');
% % save(filename, 'prolate_true');


