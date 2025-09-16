import pandas as pd

# Cargar los archivos, usando el método correcto para cada tipo
df1 = pd.read_excel('C:\\NAS_PAU\\TFG\\PGA\\BuscarInstagram.xlsx', engine='openpyxl')
df2 = pd.read_excel('C:\\NAS_PAU\\TFG\\PGA\\PGAInformacionjugadoresTotal.xlsx', engine='openpyxl')
df3 = pd.read_excel('C:\\NAS_PAU\\TFG\\PGA\\PGAprofiles.xlsx', engine='openpyxl')

# Unir los archivos en base a la columna 'Jugador'
df_merged = df1.merge(df2, on="Jugador", how="outer").merge(df3, on="Jugador", how="outer")

# Guardar el resultado en un nuevo archivo (como Excel)
df_merged.to_excel('C:\\NAS_PAU\\TFG\\PGA\\PGACompleto.xlsx', index=False, engine='openpyxl')

print("Archivos combinados correctamente en 'PGACompleto.xlsx'")

