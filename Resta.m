clear all
close all
clc

%SCRIPT PARA REALIZAR LA RESTA ENTRE LAS VELOCIDADES Y GENERAR EL
%CAMBIO DE SIST REFERENCIA
%Valentina Iturra Rosales

A = importdata("datos_stations.txt");
B = importdata("Resultados_velo.txt");

lon =A.data(:,1);
lat = A.data(:,2);

%Velocidades norte-sur
vnsA = A.data(:,4);
vnsB = B.data(:,3);
Vns = vnsA - vnsB;

%Velocidades este-oeste
vewA = A.data(:,3);
vewB = B.data(:,4);
Vew = vewA - vewB;

%Datos finales de movimiento
T = table(lon,lat,Vew,Vns,A.data(:,6),A.data(:,7),zeros(length(lon),1));
writetable(T,'mov_final.txt','WriteVariableNames', false,'Delimiter','tab')


W = table(lon,lat,A.data(:,3),A.data(:,4),A.data(:,6),A.data(:,7),zeros(length(lon),1));
writetable(W,'mov_inicial.txt','WriteVariableNames', false,'Delimiter','tab')
