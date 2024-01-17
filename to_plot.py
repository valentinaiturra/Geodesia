# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

def to_plot(t, data, pred, t_eq=None, t_at=None, name='Station', Tau=None):
    # Datos
    ew = data[:, 0]
    ns = data[:, 1]
    up = data[:, 2]
    # Estimados por el modelo de trayectoria
    Pew = pred[:, 0]
    Pns = pred[:, 1]
    Pup = pred[:, 2]
    fig1 = plt.figure(1)
    fig1.set_size_inches(11, 10)
    
    # EW
    plt.subplot(321)
    plt.plot(t, ew, '.', markersize=3, color="#00ff00")
    plt.plot(t, Pew, '-r')
    try:
        plt.plot(t_eq, np.ones(len(t_eq)) * np.min(ew), '*m', markersize=8)
    except:
        None
    try:
        plt.plot(t_at, np.ones(len(t_at)) * np.min(ew), 'D', markersize=4)
    except:
        None
    plt.ylabel('EW [mm]')
    if Tau == None:
        plt.title(name)
    else:
        plt.title("{} -- tau = {}".format(name, Tau / 0.00273785))
        
    # Residuales EW
    plt.subplot(322)
    plt.plot(t, ew - Pew, '.k', markersize=3)
    plt.plot(t, np.zeros(t.shape), '-w', markersize=3)
    try:
        plt.plot(t_eq, np.zeros(len(t_eq)), '*m', markersize=8)
    except:
        None
    try:
        plt.plot(t_at, np.zeros(len(t_at)), 'D', markersize=4)
    except:
        None
    plt.ylabel('NS [mm]')
    plt.title('Residuales')
    
    #NS
    plt.subplot(323)
    plt.plot(t, ns, '.', markersize=3, color="#00ff00")
    plt.plot(t, Pns, '-r')
    try:
        plt.plot(t_at, np.ones(len(t_at)) * np.min(ns), 'D', markersize=4)
    except:
        None
    try:
        plt.plot(t_eq, np.ones(len(t_eq)) * np.min(ns), '*m', markersize=8)
    except:
        None
    plt.ylabel('NS [mm]')
    
    # Residuales NS
    plt.subplot(324)
    plt.plot(t, ns - Pns, '.k', markersize=3)
    plt.plot(t, np.zeros(t.shape), '-w', markersize=3)
    try:
        plt.plot(t_eq, np.zeros(len(t_eq)), '*m', markersize=8)
    except:
        None
    try:
        plt.plot(t_at, np.zeros(len(t_at)), 'D', markersize=4)
    except:
        None
    plt.ylabel('NS [mm]')

    # UP
    plt.subplot(325)
    plt.plot(t, up, '.', markersize=3, color="#00ff00")
    plt.plot(t, Pup, '-r')
    try:
        plt.plot(t_eq, np.ones(len(t_eq)) * np.min(up), '*m', markersize=8)   # Teq (estrellas magentas)
    except:
        None
    try:
        plt.plot(t_at, np.ones(len(t_at)) * np.min(up), 'D', markersize=4)  #  AT (diamantes)
    except:
        None
    plt.xlabel('Tiempo')
    plt.ylabel('UP [mm]')

    # Residuales UP
    plt.subplot(326)
    plt.plot(t, up - Pup, '.k', markersize=3)
    plt.plot(t, np.zeros(t.shape), '-w', markersize=3)
    try:
        plt.plot(t_eq, np.zeros(len(t_eq)), '*m', markersize=8)
    except:
        None
    try:
        plt.plot(t_at, np.zeros(len(t_at)), 'D', markersize=4)
    except:
        None
    plt.ylabel('UP [mm]')
    plt.xlabel('Tiempo')
    plt.tight_layout()
    plt.show()