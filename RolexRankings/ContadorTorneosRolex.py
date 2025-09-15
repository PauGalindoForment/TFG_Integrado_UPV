import pandas as pd
import unicodedata

# Cargar archivos
df_torneos = pd.read_csv("C:\\NAS_PAU\\TFG\\RolexRanking\\RolexRankingtorneosjugadoraTotal.csv", sep=';')
df_jugadores = pd.read_excel("C:\\NAS_PAU\\TFG\\LPGA\\LPGA_informacionTOTAL.xlsx")

# Normalizar nombres
def normalizar(nombre):
    if isinstance(nombre, str):
        nombre = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode('utf-8')
        return nombre.lower().replace(".", "").strip()
    return ""

df_torneos["Jugadora Normalizado"] = df_torneos["Jugadora"].apply(normalizar)
df_jugadores["Nombre Normalizado"] = df_jugadores["Nombre"].apply(normalizar)

# Contar torneos jugados por cada jugador
conteo_torneos = df_torneos["Jugadora Normalizado"].value_counts().reset_index()
conteo_torneos.columns = ["Nombre Normalizado", "Torneos Jugados"]

# Unir los torneos al archivo de jugadores
df_final = df_jugadores.merge(conteo_torneos, on="Nombre Normalizado", how="left")

# Llenar con 0 los que no tengan torneos
df_final["Torneos Jugados"] = df_final["Torneos Jugados"].fillna(0).astype(int)

# Guardar resultado
df_final.drop(columns=["Nombre Normalizado"], inplace=True)
df_final.to_excel("C:\\NAS_PAU\\TFG\\RolexRanking\\jugadoras_con_torneos_RolexRanking.xlsx", index=False)
