# encoding: utf-8

import collections
import numpy as np

# Imprimir el dataframe
# print(results_df)
# Imprimir solo los 10 primeros
# print(results_df.head(10))
# Los últimos 10
# print(results_df.tail(10))
# Tipos de dato
# print(results_df.dtypes)
# Estad�sticas
# print(results_df.describe(include="all"))
# Columnas del dataframe
# print(results_df.columns)
# Cambiar nombre de columnas y guardarlo
# results_df.rename(columns={'id_de_caso': 'ID'}, inplace=True)
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
            fecha = 'NaN'
    except IndexError:
        fecha = 'NaN'
    return fecha


# Método que da casos por día ya sea de infectados muertos o recuperados
def casosxdia(columna):
    datos = []
    valores = {}
    for fecha in columna:
        try:
            fecha = fecha.split('/')
            datos.append(fecha[2] + fecha[1] + fecha[0])
        except IndexError:
            fecha = 'NaN'
    for x in datos:
        valores[x]=datos.count(x)
    valores = collections.OrderedDict(sorted(valores.items()))
    print(valores)
    return valores


# Modelo de datos exponencial
def modeloExp(t, a, b, c, d):
    return a * np.exp(b * t + c) + d


# M�todo para acumular valores
def acumulador(vector):
    datos = np.zeros(len(vector), dtype=int)
    for i in range(0, len(vector), 1):
        for j in range(0, i+1, 1):
            datos[i] = datos[i] + vector[j]
    return datos


# Método de Runge-Kutta 38
def RK38(F, X0, T, n):
    t = np.linspace(T[0], T[1], n)
    h = abs(t[2]-t[1])
    col = len(X0)
    X = np.zeros(shape=(n, col))
    X[0, :] = X0
    for i in range(n-1):
        k1 = F(t[i], X[i, :])
        k2 = F(t[i]+(1/3)*h, X[i, :]+h*(1/3)*k1)
        k3 = F(t[i]+(2/3)*h, X[i, :]+h*((-1/3)*k1 + k2))
        k4 = F(t[i]+h, X[i, :]+h*(k1-k2+k3))
        X[i+1, :] = X[i, :]+h*((1/8)*k1+(3/8)*k2+(3/8)*k3+(1/8)*k4)
    return t, X


# Casos importados, relacionados y en estudio
def casos(columna):
    ire = [0, 0, 0]
    for tipo in columna:
        if tipo == 'Importado':
            ire[0] += 1
        elif tipo == 'Relacionado':
            ire[1] += 1
        else:
            ire[2] += 1
    return ire


# Casos por edad
def edad(columna):
    edades = [0,0,0,0,0,0,0,0,0,0]
    for edad in columna:
        if edad<10:
            edades[0]+=1
        elif edad>=10 and edad<20:
            edades[1]+=1
        elif edad>=20 and edad<30:
            edades[2]+=1
        elif edad>=30 and edad<40:  
            edades[3]+=1
        elif edad>=40 and edad<50:
            edades[4]+=1
        elif edad>=50 and edad<60:
            edades[5]+=1
        elif edad>=60 and edad<70:
            edades[6]+=1
        elif edad>=70 and edad<80:
            edades[7]+=1
        elif edad>=80 and edad<90:
            edades[8]+=1
        else:
            edades[9]+=1
    return edades 
            
    