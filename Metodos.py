import pandas as pd
from sodapy import Socrata # Es un cliente de python para Socrata Open Data API .

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
results = client.get("gt2j-8ykr", limit=20000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
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
