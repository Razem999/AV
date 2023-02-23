%getCameraMeasurement will return the x y and z postion of an object, if
%there has been an object dected.
%NOTE: 

%The x,y and z postion of the measurement is taken relative to the
%CAMERA on the vehicle!
%If there has been no object detected than the program will simply return
%an empty array

%Assume that the cameras are added first onto the car
%Assume that there is 3 cameras located on the on the car
 
%ORDER OF ADDING CAMERA: 
% ADD TOP CAMERA, THEN RIGHT CAMERA, THEN LEFT CAMERA 
% ASSUME THAT WE WILL ONLY SEE ONE OBJECT PER CAMERA 

%Data: Represents the simulated data
%i: represents the row of the simulated data



function [C1xyz,C2xyz,C3xyz] = distToObjCamera2(data,i)
%Let's initialize our output variables to start    
C1xyz = []; C2xyz = []; C3xyz = [];
    

    if isempty(data(i).ObjectDetections)  
        C1xyz = [9999,9999,9999]; %NULL or 9999
        C2xyz = [9999,9999,9999];
        C3xyz = [9999,9999,9999];
    else
    
    %Lets get the size of the Object detection structure for each line of
    %of data. Lets label this as ss = structsize

    ss = size(data(i).ObjectDetections);

        for k = 1:ss(1)
            if data(i).ObjectDetections{k, 1}.SensorIndex == 1
                C1xyz = data(i).ObjectDetections{k, 1}.Measurement(1:3);
            elseif data(i).ObjectDetections{k, 1}.SensorIndex == 2
                C2xyz = data(i).ObjectDetections{k, 1}.Measurement(1:3);
            else
                C3xyz = data(i).ObjectDetections{k, 1}.Measurement(1:3);
            end
        end 

        if isempty(C1xyz)== true 
            C1xyz = [9999,9999,9999]; 
        end
        if isempty(C2xyz)== true 
            C2xyz = [9999,9999,9999]; 
        end
        if isempty(C3xyz)== true 
            C3xyz = [9999,9999,9999]; 
        end

    end



end 
     