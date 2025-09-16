import pandas as pd

# Cargar los archivos Excel
df_masculino = pd.read_excel("DatasetCompleto.xlsx")
df_femenino = pd.read_excel("DatasetCompletoFemenino.xlsx")

# Obtener las columnas comunes
columnas_comunes = df_masculino.columns.intersection(df_femenino.columns)

# Filtrar ambos dataframes para conservar solo las columnas comunes
df_masculino_comun = df_masculino[columnas_comunes]
df_femenino_comun = df_femenino[columnas_comunes]

# Unir ambos dataframes por filas (stacked)
df_unido = pd.concat([df_masculino_comun, df_femenino_comun], ignore_index=True)

# Guardar el resultado en un nuevo archivo
df_unido.to_excel("DatasetMixto.xlsx", index=False)
