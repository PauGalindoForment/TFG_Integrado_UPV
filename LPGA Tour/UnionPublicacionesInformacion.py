import pandas as pd

# Cargar los archivos Excel
df_total = pd.read_excel("LPGA_informacionTOTAL.xlsx")
df_resumen = pd.read_excel("resumen_unificado_LPGA.xlsx")

# Unir los DataFrames por la columna 'username'
df_unido = df_resumen.merge(df_total, on='username', how='left')

# Guardar el resultado en un nuevo archivo Excel
df_unido.to_excel("LPGA_DatasetCompleto.xlsx", index=False)

print("Archivo combinado guardado")
