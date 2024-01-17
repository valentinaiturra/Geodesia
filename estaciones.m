%FUNCION CREADA PARA CORTAR DATOS DE ESTACIONES Y GUARDAR EN NUEVA CARPETA,
%LUEGO DE APLICAR ESTA FUNCION SE DEBE HACER UNA SELECCiÓN DE DATOS.
%Valentina Iturra Rosales

function  estaciones(nombre, lat1, lat2,long1,long2,year1,year2,jul)
%nombre.txt , lat1 > lat2 y long1 > long2, year1< year2, jul es el dia
%juliano
%estaciones("id_coords.txt",-30,-33,-70,-72,2014,2021,213); %PARA CHILE
%estaciones("id_coords.txt",-2,-20,-33,-55,2014,2021,213); %PARA SUDESTABLE
%Recordar: para los datos de sud cambiar el nombre de stations a polo para
%evitar confusiones


datos = importdata(nombre);

A = find(datos.data(:,2) < lat1 & datos.data(:,2) > lat2);

datos.data = datos.data(A,:);
datos.textdata = datos.textdata(A,:);

A = find(datos.data(:,1) < long1 & datos.data(:,1) > long2);

datos.data = datos.data(A,:);
datos.textdata = datos.textdata(A,:);

posiciones = datos.data;
nombres = datos.textdata;

nombres = string(nombres);

mkdir("Stations")
T = table(nombres,posiciones(:,1),posiciones(:,2));
writetable(T, 'id_coords_stations.txt','WriteVariableNames', false,'Delimiter','tab') 
movefile("id_coords_stations.txt","Polo")

nombres = nombres + ".txt";


for i = 1:length(nombres)
    datos = readmatrix(nombres(i));
    years = find(datos(:,2) > year1 & datos(:,2) < year2);
    datos = datos(years,:);
    dia = find(datos(:,2) == 2015 & datos(:,3) < jul);
       if isempty(dia)
           dia = 0;
       else
           dia = dia(end);
       end
    datos= datos(dia+1:end,:);
    save (nombres(i),"datos","-ascii")
    movefile(nombres(i),"Stations")
end

