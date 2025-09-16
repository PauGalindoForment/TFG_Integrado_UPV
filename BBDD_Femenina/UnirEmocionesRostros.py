import pandas as pd

# === Cargar archivos ===
ruta_escenas = "C:/NAS_PAU/TFG/DeepFace/emociones_por_imagen_final_LPGA.csv"
ruta_publicaciones = "C:/NAS_PAU/TFG/BBDD_Femenino/DatasetCompletoFemenino.xlsx"

df_escenas = pd.read_csv(ruta_escenas, sep=';')  # Usa sep adecuado si es necesario
df_publicaciones = pd.read_excel(ruta_publicaciones)

# === Unir por 'imagen' ===
df_final = df_publicaciones.merge(
    df_escenas[['nombre_archivo', 'Rostros', 'Emocion']],
    how='left',
    on='nombre_archivo'
)

# === Guardar resultado ===
ruta_salida = "C:/NAS_PAU/TFG/BBDD_Femenino/DatasetCompletoFemenino.xlsx"
df_final.to_excel(ruta_salida, index=False)

print(f"Archivo guardado en: {ruta_salida}")
