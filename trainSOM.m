% Created on Wed July 27 10:09:46 2017
% 
% @author: Zoltan Cseresnyes
% @affiliation: Research Group Applied Systems Biology, Leibniz Institute for 
% Natural Product Research and Infection Biology – Hans Knöll Institute (HKI),
% Beutenbergstrasse 11a, 07745 Jena, Germany.
% @email: zoltan.cseresnyes@leibniz-hki.de or zcseresn@gmail.com
% 
% This is a script for creating Self Organizing Maps.
% Here we load the .csv file that contains the training data, normalize each column to 1
% then build a SOM and train it using the normalized data.
% The resulting network is then saved in a target folder (default is the source folder).
% Full details of how the script is used can be found in Kriegel et al., Cytometry A 2017. 
% If any part of the code is used for academic purposes or publications, please cite the 
% above mentioned paper.
% 
% Copyright (c) 2016-2017, 
% Leibniz Institute for Natural Product Research and Infection Biology – 
% Hans Knöll Institute (HKI)
% 
% Licence: BSD-3-Clause, see ./LICENSE or 
% https://opensource.org/licenses/BSD-3-Clause for full details

%Trains_SOM_v01.m: the first version; 27.7.17
%Trains_SOM_v02.m: allows row-wise input .csv files as well; 5.8.17
%Trains_SOM_v03.m: normalize to the largest DFT component per cell; 5.8.17


% User data
rowWiseInput = true;
withHeader = true;
trainingIterations = 1000;
originalNeighborhood = 6; 
networkSize = 12;
columnsToUse = [1 2 3 4 5 6 7 8];
columnNames = ["A" "B" "C" "D" "E" "F" "G" "H"];
rowsToUse = [1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19];
rowNames = ["F1" "F2" "F3" "F4" "F5" "F6" "F7" "F8" "F9" "F10" "F11" "F12" "F13" "F14" "F15" "F16" "F17" "F18" "F19"];

%Read in the datafile behind the main SOM : 
networkDataFolder = '/home/zoltan/Documents/Daten_sync/Software_Projects/MATLAB/Libraries/testData';
[fileNameNetworkData, folderNameNetworkData] = uigetfile(strcat(networkDataFolder, '/', '*.csv'), 'Select the datafile for the SOM network: ');
networkDataFile=importdata(strcat(folderNameNetworkData,'/',fileNameNetworkData));
if rowWiseInput == false
    netData=transpose(networkDataFile);
else
    if withHeader == true
        netData=networkDataFile.data;
    else
        netData=networkDataFile;
    end
end
    
%Prepare the normalized data file from the SOM training: 
if rowWiseInput == false
    numOfMainNetData = size(netData,1);
    C0=zeros(numOfMainNetData,4);
    for k = 1:length(columnsToUse)
        C0(:,k)=netData(1:numOfMainNetData,columnsToUse(k))/max(netData(1:numOfMainNetData,columnsToUse(k)));
    end
    mainNetImg = C0;
else
    numOfMainNetData = size(netData,2);
    C0=zeros(length(rowsToUse),numOfMainNetData);
    for k = 1:numOfMainNetData
        C0(:,k)=netData(1:length(rowsToUse),k)/max(netData(1:length(rowsToUse),k));
    end
    mainNetImg = transpose(C0);
end

% Now build and train the SOM
net = selforgmap([networkSize networkSize], trainingIterations, originalNeighborhood);
net = train(net,transpose(mainNetImg));
out = net(transpose(mainNetImg));
classes = vec2ind(out);
disp('Sum of all hits  = ' )
sum(sum(out,2)) % this number has to match the input dimension, e.g. the number of cells

% Now save the trained network for later use, default folder is the same as that of the input file
trainedSOM = net; % rename to avoid confusion with names
dots = strfind(fileNameNetworkData, '.');
filenameNoExtension = extractBefore(fileNameNetworkData,dots(length(dots)));                
savename = strcat(folderNameNetworkData,filenameNoExtension,'_SOM.mat');
save(savename,'trainedSOM');





