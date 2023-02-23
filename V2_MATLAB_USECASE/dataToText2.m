%The following function converts the simulated data into a text file
function dataToText2(data)
%assign index i = 1, to start the array at the first row of the data
i = 1; 
%Get the length of the data
DataLength = length(data);

%% INS Measurements
%lets set up our columns for position of the car (x,y,z), velocity of the
%car (x,y,z) and the distance to the object (x,y,z)
%NOTE THAT PREALLOCATION MIGHT BE NEEDED FOR EFFICIENCY
posx = []; posy = []; posz = []; velx = []; vely = []; velz = [];

%% Camera Measurements

%Camera 1
dist1xyz=[];
dist1x = []; dist1y = []; dist1z = [];

%Camera 2
dist2xyz=[];
dist2x = []; dist2y = []; dist2z = []; 

%Camera3
dist3xyz=[];
dist3x = []; dist3y = []; dist3z = []; 

    while (i<=DataLength)
        %Set up the position arrays
        posxyz = getINSposition2(data,i);
        posx = [posx; posxyz(1)]; 
        posy = [posy; posxyz(2)];
        posz = [posz; posxyz(3)];

        %Set up velocity arrays
        velxyz = getINSvelocity2(data,i);
        velx = [velx; velxyz(1)]; 
        vely = [vely; velxyz(2)];
        velz = [velz; velxyz(3)];

        %Set up the distance to object array using the Camera measuremenets
        %for Camera 1, Camera 2, and Camera 3 on the vehicle. 
        [dist1xyz,dist2xyz,dist3xyz] = distToObjCamera2(data,i);
        
        %Camera1:
        dist1x = [dist1x; dist1xyz(1)];
        dist1y = [dist1y; dist1xyz(2)];
        dist1z = [dist1z; dist1xyz(3)];
        
        %Camera2:
        dist2x = [dist2x; dist2xyz(1)];
        dist2y = [dist2y; dist2xyz(2)];
        dist2z = [dist2z; dist2xyz(3)];

        %Camera2:
        dist3x = [dist3x; dist3xyz(1)];
        dist3y = [dist3y; dist3xyz(2)];
        dist3z = [dist3z; dist3xyz(3)];

        %Increment to the next row
        i = i+1;
        end

    %Let's make the table
    T = table(posx,posy,posz,velx,vely,velz,dist1x,dist1y,dist1z,dist2x,dist2y,dist2z,dist3x,dist3y,dist3z);
    writetable(T,'tabledata.txt');
    type tabledata.txt;
end  