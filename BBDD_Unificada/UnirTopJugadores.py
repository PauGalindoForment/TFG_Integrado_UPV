import pandas as pd

# === Cargar archivos ===
ruta_escenas = "C:/NAS_PAU/TFG/DeepFace/predicciones_jugador_con_selfie_limpio.csv"
ruta_publicaciones = "C:/NAS_PAU/TFG/BBDD_Unificada/DatasetCompleto.xlsx"

df_escenas = pd.read_csv(ruta_escenas, sep=';')  # Usa sep adecuado si es necesario
df_publicaciones = pd.read_excel(ruta_publicaciones)

# === Unir por 'imagen' ===
df_final = df_publicaciones.merge(
    df_escenas[['nombre_archivo', 'brysondechambeau_ajeno', 'tyrrellhatton_ajeno', 'jonrahm_ajeno', 'joaco_niemann_ajeno','cameronsmithgolf_ajeno',	'scottie.scheffler_ajeno', 'xanderschauffele_ajeno',
                'rorymcilroy_ajeno','collin_morikawa_ajeno', 'luddeaberg_ajeno']],
    how='left',
    on='nombre_archivo'
)

# === Guardar resultado ===
ruta_salida = "C:/NAS_PAU/TFG/BBDD_Unificada//DatasetCompleto.xlsx"
df_final.to_excel(ruta_salida, index=False)

print(f"Archivo guardado en: {ruta_salida}")
