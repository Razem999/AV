% getINSposition gets the position of the car relative to the road in x, y
% and z. The data has multiple lines which can be accessed through index i
% (RECALL THAT INDEX STARTS AT 1)

%Here is how you would access the position of INSMeasurments in the data. CameraINS(1).INSMeasurements{1,1}.Velocity
%Recall that the TabyEvo will have a camera and an INS

%ADD THE INS SENSOR LAST PLEASE
function xyz = getINSposition2(data,i)
    xyz = data(i).INSMeasurements{1,1}.Position;
end 
     