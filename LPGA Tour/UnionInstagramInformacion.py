import pandas as pd

# Cargar archivos
df_info = pd.read_csv("LPGAinformacionjugadoras.csv", sep=';')
df_ig = pd.read_csv("BuscarInstagram.csv", sep=';')
df_overview = pd.read_csv("LPGAinformacion_overview.csv", sep=';')

# Función para normalizar nombres
def normalizar(nombre):
    if isinstance(nombre, str):
        return nombre.lower().replace(" ", "").replace(".", "").strip()
    return ""

# Crear claves normalizadas en cada archivo
df_info["Nombre Normalizado"] = df_info["Nombre"].apply(normalizar)
df_ig["Nombre Normalizado"] = df_ig["Jugadora"].apply(normalizar)
df_overview["Nombre Normalizado"] = df_overview["Jugadora"].apply(normalizar)

# Unir df_info + df_ig
df_merge1 = pd.merge(df_info, df_ig, on="Nombre Normalizado", how="outer")

# Crear columna final de nombre
df_merge1["Nombre"] = df_merge1["Nombre"].combine_first(df_merge1["Jugadora"])

# Eliminar columnas duplicadas
df_merge1.drop(columns=["Nombre Normalizado", "Jugadora"], inplace=True)

# Unir con df_overview
df_overview.rename(columns={"Jugadora": "Nombre"}, inplace=True)
df_final = pd.merge(df_merge1, df_overview, on="Nombre", how="outer")


# Guardar resultado final
df_final.to_csv("LPGA_informacionTOTAL.csv", index=False, sep=';', encoding='utf-8-sig')
print("Unión completada y guardada como LPGA_informacionTOTAL.csv")
