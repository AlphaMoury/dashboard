from scipy.optimize import curve_fit
import pandas as pd
import numpy as np
import Metodos
from sodapy import Socrata  # Es un cliente de python para Socrata Open Data API .

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
results_df.drop(['codigo_divipola', 'fecha_reporte_web'], axis=1, inplace=True)
# Renombrar las columnas
results_df.rename(columns={'id_de_caso': 'id',
                           'fecha_de_notificaci_n': 'fecha',
                           'ciudad_de_ubicaci_n': 'ciudad',
                           'atenci_n': 'atencion',
                           'pa_s_de_procedencia': 'pais',
                           'fis': 'fecha_sintomas',
                           'fecha_de_muerte': 'fecha_muerte'}, inplace=True)

# ---------- Columnas : id, fecha, ciudad, departamento, atencion, edad, sexo, tipo, estado, ----------
# ---------- pais, fecha_sintomas, fecha muerte, fecha_diagnostico, fecha_recuperado ------------------

# Cambio tipos de datos
results_df = results_df.astype({'id': int, 'edad': int, 'fecha_recuperado': str, 'fecha_muerte': str})

# Fallecidos, recuperados, infectados
FRI = Metodos.calculoFRI(results_df['atencion'])

# Femenino, masculino, otro
gen = Metodos.FMO(results_df['sexo'])

# -----------------Infectados------------
# Transformación de fecha
results_df['fecha_diagnostico'] = results_df['fecha_diagnostico'].transform(lambda fecha: Metodos.formatoFecha(fecha))
# Número de infectados por día y tiempo
infectados = list(Metodos.casosxdia(results_df['fecha_diagnostico']))
tiempoInfectados = np.array(range(len(infectados)))
# Datos reales, datos test y tiempo
infectadosD = infectados[:65]
tiempoInfectadosD = tiempoInfectados[:65]
infectadosT = infectados[65:]
tiempoInfectadosT = tiempoInfectados[65:]

# Regresión
paramsInfect, idn = curve_fit(Metodos.modeloExp, tiempoInfectadosD, infectadosD, maxfev=2000)

# -------------------Recuperados--------
# Transformación fecha
results_df['fecha_recuperado'] = results_df['fecha_recuperado'].transform(lambda fecha: Metodos.formatoFecha(fecha))
# Número de recuperados por día y tiempo
recuperados = list(Metodos.casosxdia(results_df['fecha_recuperado']))
tiempoRecuperados = np.array(range(len(recuperados)))
# Número acumulado de recuperados
acumuladosR = Metodos.acumulador(recuperados)

# -----------Fallecidos-----------
# Transformación fecha
results_df['fecha_muerte'] = results_df['fecha_muerte'].transform(lambda fecha: Metodos.formatoFecha(fecha))
# Número de fallecidos por día y tiempo
fallecidos = list(Metodos.casosxdia(results_df['fecha_muerte']))
tiempoFallecidos = np.array(range(len(fallecidos)))
# Número acumulado de recuperados
acumuladosF = Metodos.acumulador(fallecidos)
