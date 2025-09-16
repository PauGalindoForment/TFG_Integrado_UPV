import pandas as pd
import unicodedata

# Cargar archivos
df_torneos = pd.read_csv("torneos.csv", sep=';')
df_jugadores = pd.read_excel("jugadores_con_torneos_completo2.xlsx")

# Normalizar nombres
def normalizar(nombre):
    if isinstance(nombre, str):
        nombre = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode('utf-8')
        return nombre.lower().replace(".", "").strip()
    return ""

df_torneos["Jugador Normalizado"] = df_torneos["Jugadora"].apply(normalizar)
df_jugadores["Nombre Normalizado"] = df_jugadores["Nombre"].apply(normalizar)

# Lista de majors válidos
majors = [
    "The Chevron Championship",
    "U.S. Women's Open presented by Ally",
    "KPMG Women's PGA Championship",
    "The Amundi Evian Championship",
    "AIG Women's Open"
]

# Filtrar solo majors según la columna Evento
df_majors = df_torneos[df_torneos["Evento"].isin(majors)]

# Contar majors jugados por cada jugador
conteo_majors = df_majors["Jugador Normalizado"].value_counts().reset_index()
conteo_majors.columns = ["Nombre Normalizado", "Majors Jugados"]

# Unir los majors al archivo de jugadores
df_final = df_jugadores.merge(conteo_majors, on="Nombre Normalizado", how="left")

# Llenar con 0 los que no tengan majors
df_final["Majors Jugados"] = df_final["Majors Jugados"].fillna(0).astype(int)

# Eliminar columna auxiliar y guardar resultado
df_final.drop(columns=["Nombre Normalizado"], inplace=True)
df_final.to_excel("jugadores_con_majors.xlsx", index=False)
