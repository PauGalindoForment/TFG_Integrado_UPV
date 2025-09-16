import pandas as pd

# Cargar los archivos
df_publicaciones = pd.read_excel("C:\\NAS_PAU\\TFG\\BBDD_Femenino\\resumen_unificado_LPGA.xlsx")
df_jugadores = pd.read_excel("C:\\NAS_PAU\\TFG\\BBDD_Femenino\\Dataset_Femenino.xlsx")

# Hacer el merge usando el nombre de usuario
df_merge = df_publicaciones.merge(
    df_jugadores,
    how="left",
    left_on="username",
    right_on="username"
)

# Guardar el archivo unido
ruta_salida = "C:\\NAS_PAU\\TFG\\BBDD_Femenino\\DatosPublicacionesCompleto.xlsx"
df_merge.to_excel(ruta_salida, index=False)

print(f"Archivo guardado en: {ruta_salida}")
