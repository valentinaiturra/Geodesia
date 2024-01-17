import numpy as np
from MinCuad import MinCuadPesos as mcp
#Se carga el archivo de velocidades con las que construiremos el polo de Euler
#'Lon','lat', 've','vn'

def polo_euler(filename):
    data = np.loadtxt(filename, usecols=(0, 1, 2, 3, 4, 5), dtype=float) 
    # Longitud y latitud
    lon= data[:,0].T.flatten()
    lat= data[:,1].T.flatten()
    # Velocidad E-W y N-S
    ve=data[:,2]*0.001 # Pasamos de mm a m
    ve=ve.T.flatten()
    vn=data[:,3]*0.001
    vn=vn.T.flatten()
    # Errores asociados
    sigme=data[:,4]*0.001
    sigme=sigme.T.flatten()
    sigmn=data[:,5]*0.001 # a m 
    sigmn=sigmn.T.flatten()
    
    # Se definen los radios del geoide
    r1=6378137 # Radio ecuatorial (m)
    r2=6356752 # Eje polar del geoide (m)
    
    # Se convierten las coordenadas de grados a radianes
    lon=np.deg2rad(lon) 
    lat=np.deg2rad(lat)
    
    # Pasamos a coordenadas cartesianas la longitud y latitud
    X=r1*np.cos(lat) 
    Y=r2*np.sin(lat)
    
    r=np.sqrt(X**2 + Y**2) #Radio desde el centro del geoide a la superficie
        
    # Crear matrices de diseño G y velocidades D, y el vector de errores S
    G= np.zeros((2*len(ve),3))
    D = np.zeros((2*len(ve),1))
    S=np.zeros((2*len(ve),1))
    
    
    # Llenar las matrices G y D          
    # (eq. 11 de Goundarzi et al. 2014)
    for i in range(0, len(ve)):
        G[2*i,:]=r[i]*np.array([np.sin(lon[i]), -np.cos(lon[i]), 0])
        G[2*i+1,:]=r[i]*np.array([-np.sin(lat[i])*np.cos(lon[i]), -np.sin(lat[i])*np.sin(lon[i]), np.cos(lat[i])]);
        #Velocidades
        D[2*i,:]=vn[i]
        D[2*i+1,:]=ve[i]      
        S[2*i]=sigme[i]
        S[2*i+1]=sigmn[i]

    S=S.T.flatten() # errores
    Wd = np.diag(1/(S**2))
    
    w = mcp(G,D,Wd) # Aplicamos minimos cuadrados con pesos 
    w=w['m'] # Guardamos m en 'w'
    
    # Extraemos las componentes del Polo de Euler w_uni=(wx,wy,wz)
    wx=w[0]; wy=w[1]; wz=w[2]
    
    # Calculamos los parametros del Polo de Euler (lat,lon, magnitud)
    latp = np.rad2deg(np.arctan2(wz,np.sqrt(wx**2 +wy**2)))
    lonp = np.rad2deg(np.arctan2(wy,wx))
    omega = np.rad2deg(np.sqrt(w.T.dot(w)))*10**6; #magnitud
    
    # Velocidad predichas
    pred = G.dot(w) #G*m
    pred_n = np.zeros(len(ve))
    pred_e = np.zeros(len(ve))

    for i in range(0, len(ve)):
        pred_n[i]=pred[2*i]
        pred_e[i]=pred[2*i+1]
    
    # Finalmente el polo de euler
    euler_pole=np.zeros(3)
    euler_pole[0]=lonp
    euler_pole[1]=latp
    euler_pole[2]=omega
    
    return [euler_pole, pred_n, pred_e,latp,lonp]
    

[polo,vn_pred, ve_pred,lat,lon] = polo_euler("sud_estable.txt")
print(polo)






