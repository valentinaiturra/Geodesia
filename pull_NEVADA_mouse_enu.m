clc
clear
close all
% SCRIPT TO PULL DATA FROM THE NEVADA WEBPAGE.
% The script pulls both the metadata (latitude, longitude) and the data
% (East, North, Up)
% Note, that the data are in IGS08 format.

% Last updated 12th July 2016, Potsdam.
% This update was a slight upgrade of the script to allow choosing a range
% of stations from a global map.
% Author: Jonathan Bedford, jonrbedford@gmhthttps://www.dropbox.com/s/m9zhh7acrfof7s7/Test%201%20Geodesia%2002.docx?dl=0tps://www.dropbox.com/s/m9zhh7acrfof7s7/Test%201%20Geodesia%2002.docx?dl=0ail.com // jbed@gfz-potsdam.de




% PLOTTING THE STATIONS ON THE GLOBAL MAP
%....................................................%
aa = importdata('id_coords_all_NEVADA.txt');
stations = aa.textdata;
coords = aa.data;

figure('units','normalized','outerposition',[0.05 0.05 .9 .9]);
worldmap world; hold on;
load coastlines.mat
plotm(coastlat, coastlon)
plotm(coords(:,2),coords(:,1),'v','markersize',2,'markerfacecolor','k','color','r')

click_on = 1;
while click_on == 1;
   title('CLICK twice to select a zoom region')
   [xx,yy] = inputm(2);
   zoom_box = [[xx(1);xx(1);xx(2);xx(2);xx(1)] [yy(1);yy(2);yy(2);yy(1);yy(1)]];
   hzoom = plotm(zoom_box(:,1),zoom_box(:,2),'c-');
   
   title('CLICK to re-select zoom region,  RETURN  to advance to station selection')
   
   [advance_flag] = inputm(1);
   
   if abs(advance_flag) > 0;
       delete(hzoom);
   else
       click_on = 0;
   end        
end

close all
figure('units','normalized','outerposition',[0.05 0.05 .9 .9]);
worldmap([min(xx) max(xx)],[min(yy),max(yy)])
plotm(coastlat, coastlon)
plotm(coords(:,2),coords(:,1),'v','markersize',2,'markerfacecolor','k','color','r')

click_on = 1;
xx_running = [];
yy_running = [];
while click_on == 1;
    tit={'SELECTING STATIONS WITHIN POLYGON:';...
        'CLICK to advance selection, RETURN for more options.'};
    title(tit);
    [xx,yy] = inputm(1);
    
    if abs(xx) > 0;
        xx_running = [xx_running;xx];
        yy_running = [yy_running;yy];
        
        xx_looped = [xx_running;xx_running(1)];
        yy_looped = [yy_running;yy_running(1)];
        if numel(xx_looped) > 2;
            delete(current_box)
        end
        current_box = plotm(xx_looped,yy_looped,'-','color',[ 0.4941    0.1843    0.5569]);
        
    else
        
        tit={'SELECTING STATIONS WITHIN POLYGON:';...
            'CLICK to reset selection, RETURN to finalize selection.'};
        title(tit)
        [advance_flag] = inputm(1);
        if abs(advance_flag) > 0;
            xx_running = [];
            yy_running = [];
            xx_looped = [];
            yy_looped = [];
            delete(current_box)
        else
            click_on = 0;
        end
    end
end

% Taking stations only within selected polygon
%....................................................%

east = coords(:,1) >= 180;  % corecting for the convention of longitude
coords(east,1) = coords(east,1) - 360; % corecting for the convention of longitude


keep = inpolygon(coords(:,1),coords(:,2),yy_looped,xx_looped);
stations = stations(keep);
new_tit = ['Status: downloading.  ',num2str(0)',' of ',...
    num2str(numel(stations)),' downloaded.'];
title(new_tit);




% Preparing some variables so that the downloaded html can be transformed
% into a date.
%....................................................%

system('rm -rf ./pulled_data/*')
system('rmdir pulled_data');
system('mkdir pulled_data');



month_all = {'JAN';'FEB';'MAR';'APR';'MAY';'JUN';'JUL';'AUG';'SEP';'OCT';...
    'NOV';'DEC'};

longitudes = []; % cell arrays to be populated in the loop
latitudes = [];

plot_flag = 0;
try
for i = 1:numel(stations)
    
    
    to_disp = ['downloading data for station: ',stations{i}];
    disp(to_disp);
    
    
    % SAVING THE METADATA AS A TEMPORARY TEXT FILE
    %....................................................%
    metapath_prefix = 'http://geodesy.unr.edu/NGLStationPages/stations/';
    metapath_suffix = [stations{i},'.sta'];
    metapath = [metapath_prefix,metapath_suffix];
    aa = urlread(metapath);
    fid = fopen('meta_temp.txt','w');
    fprintf(fid,aa);
    fclose(fid);
    f_in = fopen('meta_temp.txt');
    
    % Searching line by line for the string 'Latitude:'.
    %....................................................%
    str_searched = 'Latitude:'; % string that is searched for on each line
    str_throw = 'degrees</'; % beginning of the string that you would like to throw away (to leave behind just numbers)
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
    str_throw = 'degrees</'; % beginning of the string that you would like to throw away (to leave behind just numbers)
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
    
    % Downloading the data to a temporary text file
    %....................................................%
    data_prefix = 'http://geodesy.unr.edu/gps_timeseries/tenv3/IGS14/';
    data_suffix = [stations{i},'.tenv3'];
    datapath = [data_prefix,data_suffix];
    aa = urlread(datapath);
    fid = fopen('data_temp.txt','w');
    fprintf(fid,aa);
    fclose(fid);
    f_in = fopen('data_temp.txt');
            
    % Some stations start with numbers, and this messes up the later
    % separation of string and nunbers in the 'importdata' function call.
    % Therefore, we will here add an x to the beggining of each line when
    % we have a station name starting with a number.
    if numel(str2num(aa(1))) > 0
        
        % making a while loop that will go through adding lines to a new
        % text file called 'xdata_temp.txt'
        xfid = fopen('xdata_temp.txt','w');
        carry_on = 1;
        while carry_on == 1
            cc = fgetl(f_in);
            if cc ~= -1
                cc_new = ['x',cc];
                fprintf(xfid,'%s\r\n',cc_new)
            else
                fclose(xfid);
                carry_on = 0;
            end
        end
        
        % now re-naming the xdata_temp.txt as data_temp.txt : This in fact
        % will overwrite the original data_temp.txt (which had the wrong
        % format for the importdata function).
        system('mv xdata_temp.txt data_temp.txt')
        
    end
                
    fclose(f_in);
        
    
    
    % Reading in the temporary data file and organizing into format:
    % jjjj, mm, dd, e(metres), n, u, sig_e(metres), sig_n, sig_u
    % NB// readme of the downloaded text file format can be found on metadata
    % page.
    %....................................................%
    aa = importdata('data_temp.txt');
    datestring = aa.textdata(:,2); datestring(1) = [];
    aa = aa.data; % taking only the numeric information from the file.
    
    % converting 'datestring' to yyyy mm dd
    yyyy = zeros(size(aa,1),1);
    mm = zeros(size(aa,1),1);
    dd = zeros(size(aa,1),1);
    for j = 1:numel(datestring);
        if str2num(datestring{j}(1:2)) > 80 % quick fix for years starting before 2000
            yyyy(j) = 1900 + str2num(datestring{j}(1:2));
        else
            yyyy(j) = 2000 + str2num(datestring{j}(1:2));
        end
        dd(j) = str2num(datestring{j}(6:7));
        for k = 1:numel(month_all);
            cc = findstr(month_all{k},datestring{j}(3:5));
            if numel(cc) > 0;
                mm(j) = k;
            end
        end
    end
    
    % extracting e n u (m) (enu) and errors (sig_enu)
    enu = [aa(:,7) aa(:,9) aa(:,11)];
    enu = enu - repmat(enu(1,:),size(enu,1),1);
    sig_enu = aa(:,13:15);
    
    %enu = [enu(:,3),enu(:,1),-enu(:,2)];
    %sig_enu = [sig_enu(:,3),sig_enu(:,1),sig_enu(:,2)];
    
    
    if plot_flag == 1
        % temporarily plotting
        jjj_days = datenum([yyyy mm dd]);
        figure
        title('EAST')
        plot(jjj_days,enu(:,1),'b.')
        datetick('x','mm-yyyy')
        title('EAST')
        pause
        figure
        title('NORTH')
        plot(jjj_days,enu(:,2),'b.')
        datetick('x','mm-yyyy')
        title('NORTH')
        pause
        figure
        title('UP')
        plot(jjj_days,enu(:,3),'b.')
        datetick('x','mm-yyyy')
        title('UP')
        pause
        close all
    end
    
    % Saving the pulled data
    %....................................................%
    %to_save = [yyyy mm dd enu sig_enu];
    
    % Format date
    
%     jd=datenum(yyyy,mm,dd);
%     [doy,yr]=jd2doy(jd);
%     dy=round(doy);
         
    
    D = datetime(yyyy,mm,dd)
    DOY = day(D, 'dayofyear')
    
    %output
    save_path = ['./pulled_data/',stations{i},'.txt'];
    fid = fopen(save_path,'w');
        
    for ii=1:length(yyyy)
    fprintf(fid,'%4s %u %u %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f\n',...
    stations{i},yyyy(ii),DOY(ii),1000*enu(ii,1),1000*enu(ii,2),1000*enu(ii,3),1000*sig_enu(ii,1),1000*sig_enu(ii,2),1000*sig_enu(ii,3));
    end
    
    longitudes(i) = lon; latitudes(i) = lat;
    
    %save(save_path,'to_save','-ascii','-double')
    
    
    
    % Updating title on plot
    %....................................................%
    new_tit = ['Status: downloading.  ',num2str(i),' of ',...
        num2str(numel(stations)),' downloaded.'];
    title(new_tit);
    disp(new_tit);
    
    fopen('all')
    fclose('all')
       
end
end
% Saving the station list with coords
%....................................................%

save_path = ['./pulled_data/id_coords.txt'];
fid = fopen(save_path,'w');
for i = 1:numel(longitudes);
    fprintf(fid,'%s %2.2f %2.2f \r\n',stations{i},longitudes(i),latitudes(i));
end
fclose(fid);
    
new_tit = ['Status: download completed.'];
title(new_tit);
