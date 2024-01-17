clc
clear
close all

% Go to http://geodesy.unr.edu/NGLStationPages/GlobalStationList
% Copy and paste the list of stations into a text file and save the file
% as 'all_names'




% GETS THE METADATA OF ALL GLOBAL cGPS of the NEVADA network
all_stations = importdata('all_names');

longitudes = [];
latitudes = [];
names = {};
counter = 0;

for i = 1:numel(all_stations); % outer loop
    bb = strsplit(all_stations{i});
    for j = 1:numel(bb);
        metapath_prefix = 'http://geodesy.unr.edu/NGLStationPages/stations/';
        metapath_suffix = [bb{j},'.sta'];
        metapath = [metapath_prefix,metapath_suffix];
        
        works = 1;
        
        try
            
            aa = urlread(metapath);
            fid = fopen('meta_temp.txt','w');
            fprintf(fid,aa);
            fclose(fid);
            f_in = fopen('meta_temp.txt');
            
            % Searching line by line for the string 'Latitude:'.
            %....................................................%
            str_searched = 'Latitude:'; % string that is searched for on each line
            str_throw = '</'; % beginning of the string that you would like to throw away (to leave behind just numbers)
            keep_looking = 1;
            while keep_looking == 1
                new_line = fgets(f_in); % looks at the next line of the input file, 'f_in'
                isthere = findstr(new_line,str_searched);
                if numel(isthere) > 0;
                    rhs = new_line(isthere+length(str_searched):end); % chops the line (whic%....................................................%h is a string) after the final character of searched-for string
                    end_point = findstr(rhs,str_throw)-1; % recovers the a point of the cut string, rhs, where the string will again be cut to remove unwanted characters.
                    lat = str2num(rhs(1:end_point))
                    keep_looking = 0;
                end
            end
            
            
            % Searching line by line for the string 'Longitude:'.
            %....................................................%
            str_searched = 'Longitude:'; % string that is searched for on each line
            str_throw = '</'; % beginning of the string that you would like to throw away (to leave behind just numbers)
            keep_looking = 1;
            while keep_looking == 1
                new_line = fgets(f_in); % looks at the next line of the input file, 'f_in'
                isthere = findstr(new_line,str_searched);
                if numel(isthere) > 0;
                    rhs = new_line(isthere+length(str_searched):end); % chops the line (which is a string) after the final character of searched-for string
                    end_point = findstr(rhs,str_throw)-1; % recovers the a point of the cut string, rhs, where the string will again be cut to remove unwanted characters.
                    lon = str2num(rhs(1:end_point))
                    keep_looking = 0;
                end
            end
            
            fclose(f_in);
            
            counter = counter +1
            
            longitudes(counter) = lon;
            latitudes(counter) = lat;
            names{counter} = bb{j};
            
        end
        
    end
end

% Saving the station list with coords
%....................................................%

save_path = ['./id_coords_all_NEVADA.txt'];
fid = fopen(save_path,'w');
for i = 1:numel(longitudes);
    fprintf(fid,'%s %2.2f %2.2f \r\n',names{i},longitudes(i),latitudes(i))
end
fclose(fid)
