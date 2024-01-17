#!/bin/bash

# Definimos las constantes que se usaran en todo el script para no tener que escribirlas todo el tiempo
name="mapa_vectores.ps" # Nombre con el que se guardaran los mapas
r="-75/-69/-33/-29" # Región a utilizar, de la cual deben descargar la grilla desde GMRT
j="M12" # UTM
paleta="ETOPO1.cpt" # Nombre del archivo de la paleta cpt descargada
grid_file=topo.grd # Archivo de la grilla descargada

# Creamos grilla de intensidad para iluminacion
gmt grdgradient ${grid_file} -Nt1 -A15 -Gbi.grd
gmt grdmath 0.20 bi.grd MUL = int.grd # Multiplicamos la grilla por 0.20 para suavizarla, reduce magnitud
grid_I_file=int.grd

#Creamos el marco del mapa
gmt psbasemap -R${r} -J${j} -Ba5g2f1 -Xc -Yc -K -P > ${name}
#Incluimos la grilla y paleta definidas previamente e iluminamos la topografía
gmt grdimage topo.grd  -I${grid_I_file} -R -J -B -C${paleta} -O -K >> ${name}
#Graficamos la línea de costa
gmt pscoast -R${r} -J${j} -Ba5g2f1 -Dh -W0.3,0 -N1 -I4/0.1,39/64/139 -O -K  -P >> ${name}
# Graficamos la fosa con el archivo trench-chile
gmt psxy trench-chile -R -J -O -W0.2p -Sf0.5i/0.1i+r+t+o1  -Gwhite  -B -K  >> ${name}

# Epicentro del terremoto
echo "-71.741 -31.637" | gmt psxy -R${r} -J${j} -Sa0.5C -W0.5p,0 -Gyellow  -O -K>> ${name}

# Iterar sobre las filas del archivo usando un bucle for
for ((i=1; i<=9; i++))
do
	#Agregamos puntos rojos para las estaciones
	awk -v num=$i 'NR==num {print $2, $3}' id_coords_stations.txt | gmt psxy -R${r} -J${j} -Sc0.2C -W0.5p,0 -Gred  -O -K>> ${name}
done

#Comunas
#Simbolo
echo "-71.338 -29.9532" | gmt psxy -R${r} -J${j} -Sd0.2C -W0.5p,0 -Gblue  -O -K>> ${name}
echo "-71.1683 -31.6327" | gmt psxy -R${r} -J${j} -Sd0.2C -W0.5p,0 -Gblue  -O -K>> ${name}
#Capital regional
echo "-71.252 -29.9027" | gmt psxy -R${r} -J${j} -Sc0.2C -W0.5p,0 -Ggreen  -O -K>> ${name}

#Leyenda
echo -74.9 -29.1 "Leyenda" |  gmt pstext -R${r} -J${j}  -F+f10p,Courier-Bold,black+jLM -Gwhite -O -K  >> ${name}
echo -74.8 -29.4 | gmt psxy -R${r} -J${j} -Sa0.5C -W0.5p,0 -Gyellow  -O -K>> ${name}
echo -74.8 -29.6 | gmt psxy -R${r} -J${j} -Sc0.2C -W0.5p,0 -Gred  -O -K>> ${name}
echo -74.8 -29.8 | gmt psxy -R${r} -J${j} -Sd0.2C -W0.5p,0 -Gblue  -O -K>> ${name}
echo -74.8 -30 | gmt psxy -R${r} -J${j} -Sc0.2C -W0.5p,0 -Ggreen  -O -K>> ${name}

echo -74.6 -29.4 "Terremoto 8.4 Mw" |  gmt pstext -R${r} -J${j}  -F+f8p,Courier,black+jLM -Gwhite -O -K  >> ${name}
echo -74.6 -29.6 "Estaciones" |  gmt pstext -R${r} -J${j}  -F+f8p,Courier,black+jLM -Gwhite -O -K  >> ${name}
echo -74.6 -29.8 "Comunas" |  gmt pstext -R${r} -J${j}  -F+f8p,Courier,black+jLM -Gwhite -O -K  >> ${name}
echo -74.6 -30 "Capital Regional" |  gmt pstext -R${r} -J${j}  -F+f8p,Courier,black+jLM -Gwhite -O -K   >> ${name}

gmt psvelo mov_final.txt -R${r} -J${j} -W0.25,black -Gblack -Se0.1/0.5 -O -N  -P >> ${name}

# Convertir a png
gmt psconvert ${name} -A -Tg -V
