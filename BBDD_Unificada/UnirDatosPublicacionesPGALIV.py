import pandas as pd
import numpy as np

pga_path = 'C:\\NAS_PAU\\TFG\\BBDD_Unificada\\resumen_unificado_PGA.xlsx'
liv_path = 'C:\\NAS_PAU\\TFG\\BBDD_Unificada\\resumen_unificado_LIV.xlsx'

# Leer los archivos
df_pga = pd.read_excel(pga_path)
df_liv = pd.read_excel(liv_path)

df_pga['tour'] = 'PGA'
df_liv['tour'] = 'LIV'

# Concatenar los dos DataFrames
df_combinado = pd.concat([df_pga, df_liv], ignore_index=True)

# Guardar el archivo combinado
df_combinado.to_excel('DatosPublicacionesPGALIV_TOTALlimpio.xlsx', index=False)

print("Archivos unidos")
