import numpy as np
import pandas as pd
def directo(lat,lon,latp,lonp,omega):

  # Calcula el vector de velocidad de la placa local dados la posición y la posición y velocidad del Polo de Euler

    # ENTRADAS:
    # lat, lon -> posición del punto donde se desea calcular la velocidad
    # latp, lonp, omega -> posición y velocidad del Polo de Euler

    # Las latitudes y longitudes están en grados
    # Omega está en grados por millón de años

    # SALIDA:
    # v1 = [vn, ve, vd]' velocidad en las direcciones norte, este y vertical
    # (referido al punto p) en mm/año.


    RT = 6370*10**(6) # Radio de la tierra 
    
    # convertir de grados a radianes
    latr=np.deg2rad(lat)
    lonr=np.deg2rad(lon)
    latpr=np.deg2rad(latp)
    lonpr=np.deg2rad(lonp)
    
    omega = omega*10**(-6)*(np.pi/180) # convertir a radianes por año
    
    # Convertir a coordenadas cartesianas
    # Punto
    P = np.array([
    np.cos(latr) * np.cos(lonr),  # Componente X (Este)
    np.cos(latr) * np.sin(lonr),  # Componente Y (Norte)
    np.sin(latr)                 # Componente Z (Arriba y abajo)
    ]).T  # T para transponer el vector

    # Polo de Euler 
    EP = np.array([
    np.cos(latpr) * np.cos(lonpr),  # Componente X (Este)
    np.cos(latpr) * np.sin(lonpr),  # Componente Y (Norte)
    np.sin(latpr)                  # Componente Z (Arriba y abajo)
    ]).T *omega
    
    # R*p
    VC=RT*np.cross(EP,P)
    #rotate to local coordinate system
     
    T=np.zeros((3,3));
    T[0, 0] = -np.sin(latr) * np.cos(lonr)
    T[1, 0] = -np.sin(lonr)
    T[2, 0] = -np.cos(latr) * np.cos(lonr)
    T[0, 1] = -np.sin(latr) * np.sin(lonr)
    T[1, 1] = np.cos(lonr)
    T[2, 1] = -np.cos(latr) * np.sin(lonr)
    T[0, 2] = np.cos(latr)
    T[1, 2] = 0
    T[2, 2] = -np.sin(latr)

     
    v1=T.dot(VC)
    return v1

with open('id_coords_stations.txt', 'r') as file:
    lines = file.readlines()
    data = [line.strip().split() for line in lines]

coordenadas = pd.DataFrame(data, columns=['Nombre', 'Longitud', 'Latitud'])
long = coordenadas['Longitud'].astype(float)
lat = coordenadas['Latitud'].astype(float)

n = len(long)-1  # Número de elementos en la lista
r = list(range(0, n + 1))
coords = r


resultados = pd.DataFrame(columns=['Vns','Vew','Vup'])



for a in coords:
    v = directo(lat[a],long[a], -1.89669422e+01, -1.34310380e+02,1.23512588e-01)
    extraccion = {'Vns': v[0],'Vew':v[1],'Vup':v[2]}
    resultados = pd.concat([resultados, pd.DataFrame([extraccion])], ignore_index=True)
    
resultados = pd.concat([coordenadas, resultados], axis=1)
                       
resultados.to_csv('Resultados_velo.txt', index=False, sep='\t', float_format='%.4f')
