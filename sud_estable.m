%FUNCION CREADA PARA RECORTAR DATOS DE SUDAMERICA ESTABLE, PARA INCLUIR
% SOLO DATOS DE MOVIMIENTO HORIZONTAL.
%Valentina Iturra Rosales

function sud_estable(nombre)
%sud_estable("datos_polo.txt");

A = importdata(nombre);

A= A.data;

T = table(A(:,1),A(:,2),A(:,3),A(:,4),A(:,6),A(:,7));
writetable(T, 'sud_estable.txt','WriteVariableNames', false,'Delimiter','tab')