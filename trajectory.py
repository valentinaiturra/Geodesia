# -*- coding: utf-8 -*-
"""
Trayectory model. Bevis & Brown (2014)
Joaquín Hormazabal M.
2021
"""

import numpy as np
import pylab as pl
from FG import G_matrix as FG # crea las funciones bases para armar la matriz G
from to_plot import to_plot as pt # para plotear las series de tiempo
import time
from MinCuad import MinCuadPesos as mmc # minimos cuadrados con pesos
from datetime import datetime, timedelta # ordenar los tiempos
import pickle

def toYearFraction(date):
    def sinceEpoch(date):  # returns seconds since epoch
       return time.mktime(date.timetuple()) # Segundos transcurridos desde date

    s = sinceEpoch # segundos

    year = date.year # Extrae el año de la fecha
    startOfThisYear = datetime(year=year, month=1, day=1) # Primer dia del año acctual
    startOfNextYear = datetime(year=year + 1, month=1, day=1) # Primer dia del año siguiente

    yearElapsed = s(date) - s(startOfThisYear) # Segundos transcurridos desde el inicio de año
    yearDuration = s(startOfNextYear) - s(startOfThisYear)
    fraction = yearElapsed / yearDuration

    return date.year + fraction # Devuelve el año fraccional

def extract_data(ts_file, t_cut = False): # se toma los datos de una estación, t_cut por si se quiere recortar la serie
    name = ts_file[-8:-4] # Se extrae el nombre de la estación desde el nombre del archivo
    data = np.loadtxt(ts_file, usecols=(1, 2, 3, 4, 5, 6, 7, 8), dtype=float) # Se cargan los datos, tomando desde la columna 1 a la 8
    year = data[:, 0] # La primera columna es el año
    days = data[:, 1] # La 2 columna son los dias julianos
    
    # Crea objetos datetime a partir de los valores de año y día.
    dates = [datetime(year=int(yr), month=1, day=1) + timedelta(days=int(days[i])-1)  # Convierte la lista de fechas en un arreglo numpy.
             for i, yr in enumerate(year)]
    dates = np.array(dates)  # Convierte la lista de fechas en un arreglo numpy.
    
    t = np.array([toYearFraction(date_i) for date_i in dates]) # Calcula el valor t (año fraccional) para cada fecha.
    if t_cut != False:
        ind = np.where(t >= t_cut)  # Filtra los datos según t_cut si se proporciona.
    else:
        ind = np.where(t >= t[0])  # Si no se proporciona t_cut, incluye todos los datos a partir del primer t.
        
    # Extrae columnas relevantes de datos y las apila en un arreglo numpy.
    ew = data[ind, 2].T.flatten()
    ns = data[ind, 3].T.flatten()
    up = data[ind, 4].T.flatten()
    sigm_ew = data[ind, 5].T.flatten() 
    sigm_ns = data[ind, 6].T.flatten() 
    sigm_up = data[ind, 7].T.flatten() 
    datas = np.vstack((t,ew, ns, up, sigm_ew, sigm_ns, sigm_up)).T

    return {'station' : name , 'data': datas}

def Trajectory(ts_file, t_eq = None ,tau = None, t_at = False , new_at = False, Do_plot = False,
               t_cut = False):
    name = ts_file[-8:-4]
    data = np.loadtxt(ts_file, usecols=(1, 2, 3, 4, 5, 6, 7, 8), dtype=float)
    year = data[:, 0]
    days = data[:, 1]
    dates = [datetime(year=int(yr), month=1, day=1) + timedelta(days=int(days[i])-1)
             for i, yr in enumerate(year)]
    dates = np.array(dates)
    t = np.array([toYearFraction(date_i) for date_i in dates])
    if t_cut != False:
        ind = np.where(t >= t_cut)
    else:
        ind = np.where(t >= t[0])
    t = t[ind]
    
    # Extrae las componentes EW, NS, UP y las incertidumbres
    ew = data[ind, 2].T.flatten()
    ns = data[ind, 3].T.flatten()
    up = data[ind, 4].T.flatten()
    sigm_ew = data[ind, 5].T.flatten()
    sigm_ns = data[ind, 6].T.flatten()
    sigm_up = data[ind, 7].T.flatten()
    
    # Si t_at es True, intenta extraer tiempos AT del archivo
    if t_at == True:
        t_at = extract_at(name, t_cut = t_cut)
    else:
        t_at = []
        
    # Inicializa una lista para almacenar los tiempos donde hay saltos    
    idx_jump = []
    iteration = 0 # 
    while (idx_jump != None) and (not not idx_jump) or (iteration == 0):
        pl.close()
        NJ = len(idx_jump)
        for i in range(NJ):
            t_at.append(idx_jump[i][0])

        G_all = FG(t,tau = tau, t_eq = t_eq, t_at = t_at) # Se llama a FG, donde se creo la matriz G
        G = np.hstack((G_all['g_lineal'], G_all['g_annual'], G_all['g_heavis_at'],
                   G_all['g_heavis_eq'], G_all['g_post'])) # Se juntan todas las componentes de la matriz G
        Iew = mmc(G, ew, np.diag(1/(sigm_ew**2))) # Se llama a la función para calcular minimos cuadrados con pesos
        Ins = mmc(G, ns, np.diag(1/(sigm_ns**2)))
        Iup = mmc(G, up, np.diag(1/(sigm_up**2)))

        # Obtiene los m estimados
        Mew = Iew['m']
        Mns = Ins['m']
        Mup = Iup['m']
        
        # Multiplica por G (d = G*m)
        Pew = G.dot(Mew)
        Pns = G.dot(Mns)
        Pup = G.dot(Mup)
        
        # Si Do_plot es True, genera un gráfico de las predicciones y datos observados
        if Do_plot == True:
            datas = np.vstack((ew,ns,up)).T
            pred = np.vstack((Pew,Pns,Pup)).T
            pt(t, datas, pred, t_eq=t_eq, t_at=t_at, name=name)
            
            # Si new_at es True, permite la interacción para agregar nuevos tiempos AT
            if new_at == True:
                idx_jump = pl.ginput(20, timeout = 20)
                pl.show()
            else:
                idx_jump = None
                pl.show()       
        else:
            idx_jump = None
        iteration = iteration + 1
    datas = np.vstack((t, ew, ns, up, sigm_ew, sigm_ns, sigm_up)).T

    # Si se detectaron cambios en más de una iteración, guarda los tiempos de cambio en un archivo pickle
    if iteration > 1:
        PickleFilename = f"./jumps_python/{name}_jump.pickle"
        PickleFile = open(PickleFilename, 'wb')
        data2save = {}
        data2save['t_at'] = t_at
        pickle.dump(data2save, PickleFile, pickle.HIGHEST_PROTOCOL)
        PickleFile.close()
        
    # Error cuadratico medio ponderado
    wrms_e = np.sqrt(sum((Pew - ew)**2 / sigm_ew**2 ) / sum(1/ sigm_ew**2))
    wrms_n = np.sqrt(sum((Pns - ns)**2 / sigm_ns**2 ) / sum(1/ sigm_ns**2))
    wrms_u = np.sqrt(sum((Pup - up)**2 / sigm_up**2 ) / sum(1/ sigm_up**2))

    return {'Param_ew' : Iew, 'Param_ns' : Ins, 'Param_up' : Iup,
            'fg_all' : G, 'fg' : G_all, 'new_jumps' : idx_jump,
            'data' : datas,
            'wrms_e': wrms_e, 'wrms_u': wrms_u, 'wrms_n': wrms_n }

