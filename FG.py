"""
Trayectory model. Bevis & Brown (2014)
Joaquín Hormazabal M.
2021{}
"""

import numpy as np

def Heaviside(t, t0): # t0 sera el tiempo cuando ocurre el sismo
    n = t.shape # Cuantos elementos tengo
    H = np.zeros((n)) # Ceros con la misma forma que t
    idx = np.where(t >= t0) # Donde t > t0, momentos despues de que ocurra t0
    H[idx] = 1 #  Donde t > t0 = 1

    return H

def post(t, t_eq, tau):
    Nx = t.shape[0] # Cuantos elementos tengo
    idx = np.where(t >= t_eq)  # t_eq,  tiempo de  un sismo
    log_post = np.zeros((Nx, )) # Crear un arreglo 'log_post' de ceros con longitud Nx
    log_post[idx] = np.log(1 + ((t[idx] - t_eq )/ (tau/365.25)))  # donde t>t_eq, calcular decaimiento log

    return log_post

def G_matrix(t, tau = None, t_eq = None, t_at = None):
    t = t.flatten()
    # Lineal component
    Nx = t.shape[0]
    g_lineal = np.zeros((Nx, 2))
    g_lineal[:, 0] = 1 # Rellena  la primera columna con 1
    g_lineal[:, 1] = t - t[0] # delta t
    # Annual component
    g_annual = np.zeros((Nx, 4)) # matriz de 0, de Nx filas y 4 columnas 
    g_annual[:, 0] = np.sin(2 * np.pi * t)
    g_annual[:, 1] = np.cos(2 * np.pi * t)
    g_annual[:, 2] = np.sin(4 * np.pi * t)
    g_annual[:, 3] = np.cos(4 * np.pi * t)
    # Heavis eq component
    if t_eq:
        for i in range(len(t_eq)): #  recorre cada elemento
            if (t[0] < t_eq[i]): #  si el primer valor de t es menor que el valor actual de t_eq (el evento no ha ocurrido)
                g_heavis_eq = np.array([], dtype=np.int64).reshape(Nx,0) # Crear una matriz vacía 
            else:
                t_eq = t_eq[i+1:] # Si no, se elimina ese evento de t_eq para que no se considere en las siguientes iteraciones
        N_eq = len(t_eq)
        g_heavis_eq = np.zeros((Nx, N_eq))  # Para almacenar las componentes de la función Heaviside
        for i in range(N_eq):
            g_heavis_eq[:,i] = Heaviside(t, t_eq[i]) # Calcula  Heaviside
    else:
        g_heavis_eq = np.array([], dtype=np.int64).reshape(Nx,0) # matriz vacia
    # Heavis AT component
    try:
        N_at = len(t_at) # Cantidad de at
        g_heavis_at = np.zeros((Nx, N_at)) 
        for i in range(N_at):
            g_heavis_at[:,i] = Heaviside(t, t_at[i]) # Calcula Heaviside
    except:
        g_heavis_at = np.array([], dtype=np.int64).reshape(Nx,0) # Matriz vacía
    # Postseismic component
    try:
        N_eq = len(t_eq)
        g_post = np.zeros((Nx,N_eq)) # Matriz para las componentes post sismicas
        try:
            a = tau.shape # Forma de Tau
        except AttributeError:
            tau = np.ones(20,) # Si tau no tiene forma, crea un Tau con 20 unos
        for i in range(N_eq):
            g_post[:,i] = post(t,t_eq[i],tau[i]) # Calcula post llamando a la función
    except:
        g_post = np.array([], dtype=np.int64).reshape(Nx,0) # Crea una matriz vacía

    return {'g_lineal' : g_lineal, 'g_annual' : g_annual, 'g_heavis_at' : g_heavis_at,
            'g_heavis_eq' : g_heavis_eq, 'g_post' : g_post}

