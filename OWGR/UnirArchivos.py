import pandas as pd
import os

# Ruta de la carpeta donde están los archivos CSV
carpeta = 'C:\\NAS_PAU\\TFG\\OWGR\\JugadorFoto'
archivo_nuevo = 'C:\\NAS_PAU\\TFG\\OWGR\\JugadorFoto\\OWGRJugadorFoto.csv'

# Lista para almacenar los DataFrames
dataframes = []

# Leer todos los archivos CSV en la carpeta
for archivo in os.listdir(carpeta):
    if archivo.endswith(".csv"):  
        ruta_completa = os.path.join(carpeta, archivo)
        try:
            df = pd.read_csv(ruta_completa, encoding="utf-8") 
        except UnicodeDecodeError:
            df = pd.read_csv(ruta_completa, encoding="latin1")  
        dataframes.append(df)

# Unir todos los DataFrames en uno solo
df_final = pd.concat(dataframes, ignore_index=True)

# Guardar el archivo final en UTF-8
df_final.to_csv(archivo_nuevo, index=False, encoding="utf-8")

print("Archivos CSV unidos exitosamente en 'archivo_unido.csv'.")