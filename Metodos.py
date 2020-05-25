import collections
import numpy as np


# Imprimir el dataframe
# print(results_df)
# Imprimir solo los 10 primeros
# print(results_df.head(10))
# Lós últimos 10
# print(results_df.tail(10))
# Tipos de dato
# print(results_df.dtypes)
# Estadísticas
# print(results_df.describe(include="all"))
# Columnas del dataframe
# print(results_df.columns)
# Cambiar nombre de columnas y guardarlo
# results_df.rename(columns={'id_de_caso': 'ID'},inplace=True)
# Otra manera de obtener información
# print(results_df.info())
# Convertir los tipos de datos
# results_df.astype();
# Agrupar datos
# results_df.groupby(['columna'])
# Sacar un muestro de datos
# results_df.sample(10)


# Método para calcular los fallecidos, recuperados e infectados
def calculoFRI(columna):
    fri = [0, 0, 0, 0]
    for estado in columna:
        if estado == 'Fallecido':
            fri[0] += 1
        elif estado == 'Recuperado':
            fri[1] += 1
        else:
            fri[2] += 1
    fri[3] = fri[0] + fri[1] + fri[2]
    return fri


# Método para calcular por genero
def FMO(columna):
    fmo = [0, 0, 0]
    for genero in columna:
        if genero == 'F':
            fmo[0] += 1
        elif genero == 'M':
            fmo[1] += 1
        else:
            fmo[2] += 1
    return fmo


# Método para modificar formato de fecha
def formatoFecha(fecha):
    try:
        fecha = fecha.split('T')[0].split('-')
        if len(fecha) == 3:
            fecha = fecha[2] + '/' + fecha[1] + '/' + fecha[0]
        else:
            fecha = '-'
    except IndexError:
        fecha = '-'
    if len(fecha) != 10 and len(fecha) != 1:
        fecha = '-'
    return fecha


# Método que da casos por día ya sea de infectados muertos o recuperados
def casosxdia(columna):
    datos = []
    for fecha in columna:
        try:
            fecha = fecha.split('/')
            datos.append(fecha[2] + fecha[1] + fecha[0])
        except IndexError:
            fecha = '-'
    datos_ordenadors = collections.OrderedDict(collections.Counter(datos))
    return datos_ordenadors.values()


# Modelo de datos exponencial
def modeloExp(t, a, b, c, d):
    return a * np.exp(b * t + c) + d


# Método para acumular valores
def acumulador(vector):
    datos = np.zeros(len(vector), dtype=int)
    for i in range(0, len(vector), 1):
        for j in range(0, i+1, 1):
            datos[i] = datos[i] + vector[j]
    return datos
