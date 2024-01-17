# -*- coding: utf-8 -*
# -*- coding: utf-8 -*-
"""
Trayectory model. Bevis & Brown (2014)
Joaquín Hormazabal M.
2021
"""

import numpy as np
import pandas as pd
from datetime import datetime
# importo el modelo de trayectoria y otras funciones
from trajectory import Trajectory as tj
from trajectory import toYearFraction



# corro el modelo de trayectoria
# tiene estos inputs (solo es necesario el txt de la estación)
# ts_file: ruta a la estación
# t_eq = None : si quieres ingresar un terremoto
# el formato del tiempo del terremoto es en fracción de año
# usar: "t_eq_pisagua = toYearFraction(datetime(2014,4,1))" # fecha es año mes dia
# tau = None # para los postsismicos, se ingresan en dias
# t_at = False  
# en caso de querer usar saltos (estos se guardan en un .pickle y hay que crear el directorio)
# new_at = False 
# para agregar cambios de antena (hay que dejar el Do_plot = True para esto), se abrira al figura y uno pincha donde los quiere
# Do_plot = False
# para plotear las series de tiempo con el modelo
# t_cut = False
# para cortar las series de tiempo desde un ti

t_eq_pisagua = toYearFraction(datetime(2015,9,17))
resultados = pd.DataFrame(columns=['param_ew', 'param_ns', 'param_up', 'wrms_ew','wrms_ns','wrms_up'])

# Cargar id_coords
with open('id_coords_stations.txt', 'r') as file:
    lines = file.readlines()
    data = [line.strip().split() for line in lines]

# Crea un Dataframe con los datos
coordenadas = pd.DataFrame(data, columns=['Nombre', 'Longitud', 'Latitud'])

# Convierte la longitud y latitud a números
coordenadas['Longitud'] = coordenadas['Longitud'].astype(float)
coordenadas['Latitud'] = coordenadas['Latitud'].astype(float)
# print(coordenadas)

name = coordenadas['Nombre'].astype(str)
name = name + '.txt'

n = len(name)-1  # Número de elementos en la lista
r = list(range(0, n + 1))
nom = r

# Iterar sobre las estaciones
for estacion in nom:
    param = tj(name[estacion], t_eq=[t_eq_pisagua], t_at=False, Do_plot=True, new_at=False, tau=15, t_cut=False)
    
    # Extraer los valores de interés
    param_ew = param['Param_ew']
    param_ew = param_ew['m'][1]
    param_ns = param['Param_ns']
    param_ns = param_ns['m'][1]
    param_up = param['Param_up']
    param_up = param_up['m'][1]
    wrms_n = param['wrms_n']
    wrms_e = param['wrms_e']
    wrms_u = param['wrms_u']
    extraccion = {'param_ew': param_ew, 'param_ns': param_ns, 'param_up': param_up, 'wrms_ew': wrms_e, 'wrms_ns': wrms_n, 'wrms_up': wrms_u} #diccionario con las variables
    resultados = pd.concat([resultados, pd.DataFrame([extraccion])], ignore_index=True)  

# Unir coordenadas y resultados
resultados = pd.concat([coordenadas, resultados], axis=1)

# Guardar en un archivo de texto
resultados.to_csv('datos_stations.txt', index=False, sep='\t', float_format='%.4f')

# Param tiene los "m" y "Cm"
# fg_all tiene la matriz G
# fg tiene todas las funciones bases separadas
# data tiene los datos (tiempo, ew, ns, up, sigm_Ew, sigm_ns, sigm_up)
# wrms son los errores cuadraticos medio con pesos respectivos
