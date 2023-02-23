% getINSvelocity gets the position of the car relative to the road in x, y
% and z. The data has multiple lines which can be accessed through index i
% (RECALL THAT INDEX STARTS AT 1)

function xyz = getINSvelocity2(data,i)
    xyz = data(i).INSMeasurements{1,1}.Velocity;
end 
     