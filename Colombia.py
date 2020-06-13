# encoding: utf-8

from scipy.optimize import curve_fit
import pandas as pd
import numpy as np
import Metodos
# Es un cliente de python para Socrata Open Data API.
from sodapy import Socrata
from unittest.mock import inplace

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("www.datos.gov.co", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(www.datos.gov.co,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")

# results returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("gt2j-8ykr", limit=50000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

# LIMPIEZA
# Quitar columna
results_df.drop(['fecha_reporte_web'], axis=1, inplace=True)
# Renombrar las columnas
results_df.rename(columns={'id_de_caso': 'id',
                           'fecha_de_notificaci_n': 'fecha',
                           'ciudad_de_ubicaci_n': 'ciudad',
                           'atenci_n': 'atencion',
                           'pa_s_de_procedencia': 'pais',
                           'fis': 'fecha_sintomas',
                           'fecha_de_muerte': 'fecha_muerte'}, inplace=True)

# ---------- Columnas : id, fecha, ciudad, departamento, atencion -------------
# ---------- edad, sexo, tipo, estado,pais, fecha_sintomas,  -------------------
# ---------- fecha muerte, fecha_diagnostico, fecha_recuperado ----------------

# Cambio tipos de datos
results_df = results_df.astype({'id': int, 'edad': int,
                                'fecha_diagnostico': str,
                                'fecha_recuperado': str, 'fecha_muerte': str})

# Fallecidos, recuperados, infectados
FRI = Metodos.calculoFRI(results_df['atencion'])

# Femenino, masculino, otro
gen = Metodos.FMO(results_df['sexo'])

# Importado, relacionado, en estudio
IRE = Metodos.casos(results_df['tipo'])

# Casos por edad
edad = Metodos.edad(results_df['edad'])

# -----------------Infectados------------
# Transformación de fecha
results_df['fecha_diagnostico'] = results_df['fecha_diagnostico'].apply(lambda fecha: Metodos.formatoFecha(fecha))
# Número de infectados por día y tiempo
datosI = Metodos.casosxdia(results_df['fecha_diagnostico'])
infectados = list(datosI.values())
fechasI = list(datosI.keys())
tiempoInfectados = np.array(range(len(infectados)))
# Acumulados
acumuladosI = Metodos.acumulador(infectados)
# Datos reales, datos test y tiempo
infectadosD = acumuladosI[:75]
tiempoInfectadosD = tiempoInfectados[:75]
infectadosT = acumuladosI[75:]
tiempoInfectadosT = tiempoInfectados[75:]

# Regresión
paramsInfect, idn = curve_fit(Metodos.modeloExp, tiempoInfectadosD, infectadosD, maxfev=2000)



# -------------------Recuperados--------
# Transformación fecha
results_df['fecha_recuperado'] = results_df['fecha_recuperado'].apply(lambda fecha: Metodos.formatoFecha(fecha))
# Número de recuperados por día y tiempo
datosR = Metodos.casosxdia(results_df['fecha_recuperado'])
recuperados = list(datosR.values())
tiempoRecuperados = np.array(range(len(recuperados)))
# Número acumulado de recuperados
acumuladosR = Metodos.acumulador(recuperados)
# Datos reales, datos test
recuperadosD = acumuladosR[:70]
tiempoRecuperadosD = tiempoRecuperados[:70]
recuperadosT = acumuladosR[70:]
tiempoRecuperadosT = tiempoRecuperados[70:]

# Regresión
paramsRecup, idn = curve_fit(Metodos.modeloExp, tiempoRecuperadosD, recuperadosD, maxfev=5000)

# -----------Fallecidos-----------
# Transformaci�n fecha
results_df['fecha_muerte'] = results_df['fecha_muerte'].apply(lambda fecha: Metodos.formatoFecha(fecha))
# N�mero de fallecidos por día y tiempo
datosF = Metodos.casosxdia(results_df['fecha_muerte'])
fallecidos = list(datosF.values())
tiempoFallecidos = np.array(range(len(fallecidos)))
# Número acumulado de recuperados
acumuladosF = Metodos.acumulador(fallecidos)
# Datos reales, datos test
fallecidosD = acumuladosF[:65]
tiempoFallecidosD = tiempoFallecidos[:65]
fallecidosT = acumuladosF[65:]
tiempoFallecidosT = tiempoFallecidos[65:]

# Regresión
paramsFall, idn = curve_fit(Metodos.modeloExp, tiempoFallecidosD, fallecidosD, maxfev=5000)

# ---------------- Modelo SIR --------------
# Hiperparametros
g = 1/14
b = 0.24  # (1; 1,5; 2; 2,5 y 3)
# N = 48200000
N = 26128023

# Modelo P[0]=S P[1]=I P[2]=R


def F(t, P): return np.array([-b*P[0]*(P[1]/N),
                              b*P[0]*(P[1]/N) - g*P[1],
                              g*P[1]])


# Condiciones iniciales 13 de abril
P0 = [26125247, 2776, 379]

# Tiempo
T = [0, 150]

# N�mero de puntos
n = 500

t, sol = Metodos.RK38(F, P0, T, n)

# ------------ Párametros SIR ---------
# Beta
S = 10000-acumuladosI[:35]
dSdt = Metodos.CD(tiempoInfectados[:35],S)
SI = -S[1:-1]*(acumuladosI[1:34]/10000)
beta = (dSdt/SI).mean()
#Gama
R = acumuladosR[:35]+acumuladosF[:35]
dRdt = Metodos.CD(tiempoRecuperados[:35],R)
I = acumuladosI[1:34]
gamma = (dRdt/I).mean()
