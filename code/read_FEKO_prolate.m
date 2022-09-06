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



%% Load the FEKO data

cd("G:\Rofrano_Thesis\Project\data\Prolate"); % From main drive
tar_true = readFeko('prolate_far_field.ffe');

%% Save the thing

cd("G:\Rofrano_Thesis\Project\data")
filename = strcat(t, '_prolate_ffe');
save(filename, 'tar_true');


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


