import pandas as pd

# Cargar publicaciones
ruta_datos = "C:\\NAS_PAU\\TFG\\BBDD_Femenino\\DatasetCompletoFemenino.xlsx"
df_datos = pd.read_excel(ruta_datos)

# Cargar predicciones con columnas 'selfie' y 'otro_golfista'
ruta_predicciones = "C:\\NAS_PAU\\TFG\\Deepface\\predicciones_jugadora_por_imagen_limpio_LPGA.csv"
df_pred = pd.read_csv(ruta_predicciones, sep=';')

# Fusionar por columna 'imagen'
df_completo = df_datos.merge(
    df_pred[['nombre_archivo', 'selfie', 'otro_golfista']],
    how='left',
    on='nombre_archivo'
)

# Llenar NaNs por si alguna imagen no aparece en predicciones
df_completo[['selfie', 'otro_golfista']] = df_completo[['selfie', 'otro_golfista']].fillna(0).astype(int)

# Guardar nuevo archivo Excel
ruta_salida = "C:\\NAS_PAU\\TFG\\BBDD_Femenino\\DatasetCompletoFemenino.xlsx"
df_completo.to_excel(ruta_salida, index=False)

print(f"Archivo guardado en: {ruta_salida}")

