# Geodesia: deformación cosísmica del terremoto de Illapel 2015

Tarea 1 del curso de Física, Geodesia y Tectónica (Valentina Iturra Rosales). El informe completo está en [IturraV_Tarea1_FGyT.pdf](IturraV_Tarea1_FGyT.pdf).

El objetivo es estimar el desplazamiento de 9 estaciones GPS continuas de la zona de Coquimbo/Illapel (≈29–33°S) asociado al terremoto de Illapel (Mw 8.3, 16-09-2015), expresado con respecto a **Sudamérica estable**. Para eso:

1. Se descargan las series de tiempo GPS del [Nevada Geodetic Laboratory](http://geodesy.unr.edu/) (NGL).
2. Se ajusta un **modelo de trayectoria** (Bevis & Brown, 2014) a cada estación para obtener su velocidad.
3. Con 65 estaciones de Sudamérica estable (Brasil) se calcula el **polo de Euler** de la placa (problema inverso).
4. Con ese polo se calcula la velocidad de placa en cada estación chilena (problema directo).
5. Se restan ambas velocidades para obtener el movimiento relativo a Sudamérica estable.
6. Se grafican los resultados en mapas con GMT.

Polo de Euler obtenido: **lon = −134.31°, lat = −18.97°, ω = 0.1235 °/Ma**.

---

## Estructura del repositorio

```
Geodesia/
├── README.md
├── IturraV_Tarea1_FGyT.pdf     Informe de la tarea
├── Paso a paso.txt             Notas con el orden de trabajo
│
├── get_global_meta.m           (MATLAB) Lista global de estaciones NGL
├── pull_NEVADA_mouse_enu.m     (MATLAB) Descarga de series de tiempo
├── estaciones.m                (MATLAB) Recorte de estaciones y fechas
├── sud_estable.m               (MATLAB) Prepara datos para el polo de Euler
├── Resta.m                     (MATLAB) Cambio de sistema de referencia
│
├── FG.py                       (Python) Funciones base del modelo de trayectoria
├── MinCuad.py                  (Python) Mínimos cuadrados
├── trajectory.py               (Python) Modelo de trayectoria
├── to_plot.py                  (Python) Gráficos de series de tiempo
├── example_editado.py          (Python) Corre el modelo para todas las estaciones
├── inverso.py                  (Python) Polo de Euler (problema inverso)
├── directo.py                  (Python) Velocidad de placa (problema directo)
│
├── id_coords_all_NEVADA.txt    Coordenadas de todas las estaciones NGL
├── coastlines.mat              Línea de costa para el mapa de selección
├── data_temp.txt, meta_temp.txt  Archivos temporales de la descarga
│
├── Estaciones/                 Resultados de las 9 estaciones de Chile
├── Polo/                       Datos de Sudamérica estable
└── Mapas/                      Scripts y datos de GMT
```

---

## Descripción de los archivos

### Scripts MATLAB

| Archivo | Descripción | Entrada | Salida |
|---|---|---|---|
| `get_global_meta.m` | Consulta la página de cada estación NGL y guarda su latitud y longitud. Script de J. Bedford. | `all_names` (lista de estaciones copiada desde la web de NGL) | `id_coords_all_NEVADA.txt` |
| `pull_NEVADA_mouse_enu.m` | Muestra un mapa mundial; con el mouse se elige una zona y un polígono, y se descargan las series `.tenv3` (IGS14) de las estaciones dentro de él. Convierte a mm y día juliano. Script de J. Bedford, modificado. | `id_coords_all_NEVADA.txt`, `coastlines.mat` | `pulled_data/<EST>.txt`, `pulled_data/id_coords.txt` |
| `estaciones.m` | Función `estaciones(nombre, lat1, lat2, long1, long2, year1, year2, jul)`. Filtra las estaciones por latitud/longitud y recorta las series entre `year1` y `year2`, empezando en el día juliano `jul` de 2015. | `id_coords.txt` y los `.txt` de cada estación | `Stations/<EST>.txt`, `id_coords_stations.txt` |
| `sud_estable.m` | Función `sud_estable(nombre)`. Deja solo las columnas horizontales (lon, lat, ve, vn, σe, σn). | `Polo/datos_polo.txt` | `sud_estable.txt` |
| `Resta.m` | Resta la velocidad de placa a la velocidad observada (cambio de sistema de referencia). | `Estaciones/datos_stations.txt`, `Estaciones/Resultados_velo.txt` | `mov_final.txt`, `mov_inicial.txt` |

Ejemplos de uso de `estaciones.m` (escritos en el propio archivo):

```matlab
estaciones("id_coords.txt", -30, -33, -70, -72, 2014, 2021, 213);  % Chile
estaciones("id_coords.txt",  -2, -20, -33, -55, 2014, 2021, 213);  % Sudamérica estable
```

### Scripts Python

| Archivo | Descripción |
|---|---|
| `FG.py` | Construye la matriz G del modelo de trayectoria: término lineal, términos anual y semianual, saltos (Heaviside) por sismos y cambios de antena, y decaimiento postsísmico logarítmico. |
| `MinCuad.py` | `MinCuadSimple` y `MinCuadPesos`: solución de `G·m = d` por mínimos cuadrados simples y ponderados. |
| `trajectory.py` | `Trajectory(...)`: lee la serie de una estación, ajusta las componentes EW, NS y UP y devuelve los parámetros, la matriz G y el WRMS. Incluye `toYearFraction` para pasar fechas a año fraccional. |
| `to_plot.py` | Grafica datos, modelo y residuos de las tres componentes. |
| `example_editado.py` | Corre `Trajectory` para cada estación de `id_coords_stations.txt` con el sismo de Illapel como evento. Guarda la velocidad (parámetro lineal) y el WRMS de cada componente. |
| `inverso.py` | Calcula el polo de Euler por mínimos cuadrados ponderados (ec. 11 de Goudarzi et al., 2014) a partir de `sud_estable.txt` e imprime `[lon, lat, ω]`. |
| `directo.py` | Calcula la velocidad de placa (Vns, Vew, Vup en mm/año) en cada estación usando el polo de Euler, que está escrito directamente en el código. |

Los scripts de trayectoria se basan en el código de Joaquín Hormazábal M. (2021).

### Datos y resultados

**`Estaciones/`** — Estaciones de Chile: BN17, BTO1, CMBA, CNBA, LVI1, PEDR, PFRJ, SLMC y ZAPA.

| Archivo | Contenido |
|---|---|
| `id_coords_stations.txt` | Nombre, longitud y latitud |
| `datos_stations.txt` | Velocidades del modelo de trayectoria (mm/año) y WRMS |
| `Resultados_velo.txt` | Velocidad de placa según el polo de Euler |
| `mov_inicial.txt` | Velocidades observadas en formato `psvelo` |
| `mov_final.txt` | Velocidades respecto a Sudamérica estable en formato `psvelo` |
| `Figure ... (0–8).png` | Gráficos del modelo de trayectoria de cada estación |

El formato `psvelo` de `mov_*.txt` es: `lon  lat  ve  vn  σe  σn  correlación`.

**`Polo/`** — 65 estaciones de Sudamérica estable.

| Archivo | Contenido |
|---|---|
| `id_coords_polo.txt` | Nombre, longitud y latitud |
| `datos_polo.txt` | Velocidades del modelo de trayectoria y WRMS |
| `sud_estable.txt` | Entrada de `inverso.py`: lon, lat, ve, vn, σe, σn |

**`Mapas/`**

| Archivo | Contenido |
|---|---|
| `tareando.sh` | Mapa de ubicación: topografía, fosa, epicentro, estaciones, ciudades y leyenda → `mapa.png` |
| `tareando2.sh` | Igual que el anterior, más los vectores de `mov_final.txt` → `mapa_vectores.png` |
| `topo.grd` | Grilla de topografía/batimetría (GMRT) |
| `ETOPO1.cpt` | Paleta de colores |
| `trench-chile` | Traza de la fosa Chile-Perú |
| `bi.grd`, `int.grd` | Grillas de iluminación (las regeneran los scripts) |
| `id_coords_stations.txt`, `mov_final.txt` | Copias de los archivos de `Estaciones/` |

---

## Requisitos

- **MATLAB** con el *Mapping Toolbox* (`worldmap`, `plotm`, `inputm`), necesario para `pull_NEVADA_mouse_enu.m`. Se usó R2024a.
- **Python 3** con `numpy`, `pandas` y `matplotlib`. Por ejemplo, Anaconda.
- **GMT 6** (se usó 6.3.0), más `bash` y `awk` para los scripts de mapas. En Windows sirve Git Bash o WSL.

---

## Cómo correrlo

> **Importante:** todos los scripts usan rutas relativas y buscan sus archivos en la carpeta desde donde se ejecutan. Por eso se indica desde qué carpeta correr cada paso.

### 1. Descargar los datos (MATLAB)

En la raíz del repositorio:

```matlab
pull_NEVADA_mouse_enu
```

Selecciona la zona con el mouse. Las series quedan en `pulled_data/`. Repite el proceso para la zona de Chile y para Sudamérica estable.

### 2. Recortar estaciones (MATLAB)

Copia `estaciones.m` dentro de `pulled_data/` y córrelo con los parámetros de la zona (ver ejemplos arriba). Después elimina las estaciones vacías o con problemas. Según `Paso a paso.txt`:

- **Chile:** se eliminaron ROBL (vacía), CER1, CTPC, EMAT, LNDS, OVLL, POR2, PVCA, ROB1 y TOLO.
- **Sudamérica estable:** se eliminaron FORT, MCLA, PAST, PLMS y SALV (vacías), y BOMJ y MTBA (fallas de medición).

### 3. Modelo de trayectoria (Python)

Pon en una misma carpeta `id_coords_stations.txt` y los `.txt` de cada estación. Desde esa carpeta, corre:

```bash
python ruta/a/Geodesia/example_editado.py
```

Se abrirá un gráfico por estación; hay que cerrarlo para pasar a la siguiente. El resultado es `datos_stations.txt`. Para Sudamérica estable, renombra la salida a `datos_polo.txt`.

### 4. Polo de Euler (MATLAB + Python)

Desde `Polo/`:

```matlab
sud_estable("datos_polo.txt")
```

```bash
cd Polo
python ../inverso.py
```

### 5. Velocidad de placa (Python)

Si cambió el polo de Euler, actualiza los valores en la línea de `directo.py` que llama a `directo(...)`. Luego:

```bash
cd Estaciones
python ../directo.py      # genera Resultados_velo.txt
```

### 6. Cambio de sistema de referencia (MATLAB)

Desde `Estaciones/`:

```matlab
addpath('..')
Resta                      % genera mov_final.txt y mov_inicial.txt
```

### 7. Mapas (GMT)

Copia `mov_final.txt` e `id_coords_stations.txt` a `Mapas/` y ejecuta:

```bash
cd Mapas
bash tareando.sh           # mapa.png
bash tareando2.sh          # mapa_vectores.png
```

---

## Notas y limitaciones conocidas

- **Faltan las series de tiempo de cada estación** (`BN17.txt`, `ALAR.txt`, etc.), así que los pasos 1 a 3 necesitan descargarlas de nuevo. Los pasos 4 a 7 se pueden correr con los archivos incluidos.
- `pull_NEVADA_mouse_enu.m` usa comandos de Unix (`rm`, `mv`, `rmdir`) a través de `system()`, que no funcionan en Windows sin adaptarlos. Además usa `urlread` con URLs `http://.../tenv3/IGS14/`; conviene revisar que NGL todavía las ofrezca (puede que ahora estén en `https` o en el marco IGS20).
- `estaciones.m` mueve `id_coords_stations.txt` a una carpeta `Polo`, que debe existir de antemano.
- `trajectory.py` obtiene el nombre de la estación con `ts_file[-8:-4]`, así que asume nombres de 4 caracteres. Si usas `new_at=True`, necesitas la carpeta `jumps_python/`.
- En `FG.py`, si `tau` se pasa como número (por ejemplo `tau=15`), se reemplaza por un vector de unos; en la práctica el postsísmico se calcula con τ = 1 día.
- En `inverso.py`, los pesos de las componentes norte y este están intercambiados: `vn` se pondera con `σe` y `ve` con `σn`.
- Los scripts de GMT asumen exactamente 9 estaciones (`for ((i=1; i<=9; i++))`).

## Referencias

- Bevis, M., & Brown, A. (2014). Trajectory models and reference frames for crustal motion geodesy. *Journal of Geodesy*, 88(3), 283–311.
- Goudarzi, M. A., Cocard, M., & Santerre, R. (2014). EPC: Matlab software to estimate Euler pole parameters. *GPS Solutions*, 18(1), 153–162.
- Blewitt, G., Hammond, W. C., & Kreemer, C. (2018). Harnessing the GPS data explosion for interdisciplinary science. *Eos*, 99.
