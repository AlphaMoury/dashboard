import numpy as np
import pandas as pd
import os  # Módulo da acceso a operaciones a nivel sistema operativo

# Leer el documento datos.csv
datos = pd.read_csv(os.path.join('data/COVID-19_Colombia.csv'))

# Datos de la columna Atención
datosA = datos['atención']

# Datos de la columna Fecha de notificación
datosF = datos['Fecha de notificación']


f = 0
r = 0
i = 0

for estado in datosA:
    if estado == 'Fallecido':
        f = f+1
    elif estado == 'Recuperado':
        r = r+1
    else:
        i = i+1
        
N = r+f+i


# Datos por Género
femenino = 0
masculino = 0
otro = 0

for genero in datos['Sexo']:
    if genero == 'F':
        femenino += 1
    elif genero == 'M':
        masculino += 1
    else:
        otro += 1

