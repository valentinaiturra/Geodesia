# -*- coding: utf-8 -*-

from numpy.linalg import lstsq # Para calcular la solución de mínimos cuadrados 
import numpy as np

def MinCuadSimple(G, d): # Recibe G y los datos d 
    """
    Calcula la solución de G*m = d por el método de mínimos cuadrados simples.
    Devuelve un diccionario con m y Cm.
    """
    Ndata, Npar = G.shape # Ndata es el número de datos y Npar es el número de parámetros 
    Cm = np.linalg.lstsq(G.T.dot(G), np.eye(Npar), rcond= -1)[0]  # Cm para ponderar
    m = Cm.dot(G.T.dot(d))
    return {'m': m, 'Cm': Cm}


######
def MinCuadPesos(G, d, Wx): 
    """
    Calcula la solución de Wx*G*m = Wx*d por el método de mínimos cuadrados (con pesos).
    Devuelve un diccionario con m y Cm.
    """
    return MinCuadSimple(Wx.dot(G), Wx.dot(d))