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
results_df = results_df.astype({'id': int, 'edad': int})

# Fallecidos, recuperados, infectados
FRI = Metodos.calculoFRI(results_df['atencion'])

# Femenino, masculino, otro
gen = Metodos.FMO(results_df['sexo'])

# -----------------Infectados------------
# Número de infectados por día
# print(results_df.groupby('fecha_diagnostico')['fecha_diagnostico'].count())
conteoInfect = np.array(results_df.groupby('fecha_diagnostico')['fecha_diagnostico'].count())
# Conteo desde el 11 de marzo
infectados = conteoInfect[3:]
tiempoInfectados = np.array(range(len(infectados)))

# Regresión
paramsInfect, idn = curve_fit(Metodos.modeloExp, tiempoInfectados, infectados, maxfev=2000)

# -------------------Recuperados--------
# Número de recuperados por día
# print(results_df.groupby('fecha_recuperado')['fecha_recuperado'].count())
conteoRec = np.array(results_df.groupby('fecha_recuperado')['fecha_recuperado'].count())
recuperados = conteoRec[1:-1]
tiempoRecuperados = np.array(range(len(recuperados)))

# -----------Fallecidos-----------
# Número de fallecidos por dia
# print(results_df.groupby('fecha_muerte')['fecha_muerte'].count())
conteoFall = np.array(results_df.groupby('fecha_muerte')['fecha_muerte'].count())
fallecidos = conteoFall[1:]
timempoFallecidos = np.array(range(len(fallecidos)))
