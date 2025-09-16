import pandas as pd

# Cargar los archivos CSV
eventos = pd.read_csv("LPGAeventos2024_separado.csv", sep=';')
ganancias = pd.read_csv("LPGAganancias2024_separado.csv", sep=';')

# Normalizar nombres
def normalizar(nombre):
    return nombre.lower().replace(" ", "").replace(".", "").strip()

eventos["Nombre Normalizado"] = eventos["Nombre"].apply(normalizar)
ganancias["Nombre Normalizado"] = ganancias["Nombre"].apply(normalizar)

# Merge por nombre normalizado
df_merged = pd.merge(eventos, ganancias, on="Nombre Normalizado", how="outer", suffixes=('_eventos', '_ganancias'))

# Seleccionar nombre consolidado (prioriza eventos)
df_merged["Nombre"] = df_merged["Nombre_eventos"].combine_first(df_merged["Nombre_ganancias"])

# Combinar 'País' y 'Torneos Jugados' evitando duplicados
df_merged["País"] = df_merged["País_eventos"].combine_first(df_merged["País_ganancias"])
df_merged["Torneos"] = df_merged["Torneos_eventos"].combine_first(df_merged["Torneos_ganancias"]).astype(int)

# Seleccionar columnas deseadas
columnas_finales = ["Nombre", "País", "Torneos", "Dinero"]
df_final = df_merged[columnas_finales]

# Guardar en CSV
df_final.to_csv("LPGAinformacionjugadoras.csv", index=False, sep=';', encoding='utf-8-sig')
print(" Archivo guardado ")
