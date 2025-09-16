import pandas as pd

# Cargar los archivos
df_publicaciones = pd.read_excel("C:\\NAS_PAU\\TFG\\BBDD_Unificada\\DatosPublicacionesPGALIV.xlsx")
df_jugadores = pd.read_excel("C:\\NAS_PAU\\TFG\\BBDD_Unificada\\Jugadores_PGA_LIV_Unificado.xlsx")

# Hacer el merge usando el nombre de usuario
df_merge = df_publicaciones.merge(
    df_jugadores,
    how="left",
    left_on="usuario_instagram",
    right_on="Username"
)

# Guardar el archivo unido
ruta_salida = "C:\\NAS_PAU\\TFG\\BBDD_Unificada\\DatosPublicacionesPGALIV_con_info_jugadores.xlsx"
df_merge.to_excel(ruta_salida, index=False)

print(f"Archivo guardado en: {ruta_salida}")
