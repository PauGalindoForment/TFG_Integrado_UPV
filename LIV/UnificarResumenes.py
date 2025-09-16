import os
import pandas as pd

RUTA_PRINCIPAL = 'C:\\NAS_PAU\\TFG\\LIV\\Instagram'
ARCHIVO_SALIDA = 'resumen_unificado_TODOS_NaN.xlsx'

# Columnas correctas y orden final
COLUMNAS_BUENAS = [
    'player', 'username', 'num', 'post', 'shortcode', 'fecha', 'hora', 'n_carrusel',
    'n_fotos', 'n_videos', 'visualizaciones_video', 'likes', 'comentarios', 'texto',
    'hashtags', 'is_sponsored', 'sponsor_users', 'tagged_users', 'mentions'
]

dataframes = []

for usuario in os.listdir(RUTA_PRINCIPAL):
    ruta_usuario = os.path.join(RUTA_PRINCIPAL, usuario)
    if os.path.isdir(ruta_usuario):
        archivos_csv = [f for f in os.listdir(ruta_usuario)
                        if f.endswith('.csv') and not f.startswith('0_')]

        for archivo in archivos_csv:
            ruta_csv = os.path.join(ruta_usuario, archivo)
            try:
                df = pd.read_csv(ruta_csv, sep=',', encoding='utf-8', engine='python')

                # Añadir columna 'username' si falta
                if 'username' not in df.columns:
                    df['username'] = 'NaN'

                # Asegurar todas las columnas necesarias están presentes
                for col in COLUMNAS_BUENAS:
                    if col not in df.columns:
                        df[col] = pd.NA

                # Reordenar
                df = df[COLUMNAS_BUENAS]

                dataframes.append(df)
            except Exception as e:
                print(f"⚠️ Error leyendo {ruta_csv}: {e}")

# Unir y exportar
if dataframes:
    df_unido = pd.concat(dataframes, ignore_index=True)
    df_unido.to_excel(ARCHIVO_SALIDA, index=False)
    print(f"✅ Archivo combinado exportado a '{ARCHIVO_SALIDA}' con columnas estándar.")
else:
    print("❌ No se encontraron archivos CSV válidos.")
