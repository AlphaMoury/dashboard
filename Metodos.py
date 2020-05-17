from datetime import date
from datetime import datetime


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
    fri[3] = fri[0]+fri[1]+fri[2]
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


