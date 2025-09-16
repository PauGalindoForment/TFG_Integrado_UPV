import pandas as pd
import unicodedata

# Función para normalizar nombres: elimina tildes, pasa a minúsculas, quita puntos
def normalizar_nombre(nombre):
    if not isinstance(nombre, str):
        return ""
    nombre = nombre.lower().replace(".", "").strip()
    nombre = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode('ascii')
    return nombre

# Cargar el archivo de jugadores
df_jugadores = pd.read_excel("C:\\NAS_PAU\\TFG\\BBDD_Femenino\\DatasetCompletoFemenino.xlsx")

# Cargar la clasificación oficial OWGR
df_owgr = pd.read_csv("C:\\NAS_PAU\\TFG\\RolexRanking\\rolexrankings_2024-12-30.csv", sep=';')

# Asegurarse de usar solo el nombre del jugador sin país, si hace falta
# Aquí asumimos que la columna limpia es 'Nombre Jugador Limpio'
df_owgr["Nombre Normalizado"] = df_owgr["player_name"].apply(normalizar_nombre)

# Crear diccionario: nombre → posición
dict_owgr = dict(zip(df_owgr["Nombre Normalizado"], df_owgr["rank"]))

# Normalizar nombres de los jugadores
df_jugadores["Nombre Normalizado"] = df_jugadores["Nombre"].apply(normalizar_nombre)

# Asignar posición OWGR desde el diccionario
df_jugadores["Posición Rolex Ranking"] = df_jugadores["Nombre Normalizado"].map(dict_owgr)

# Eliminar columna auxiliar si no se necesita
df_jugadores.drop(columns=["Nombre Normalizado"], inplace=True)

# Guardar archivo final
df_jugadores.to_excel("C:\\NAS_PAU\\TFG\\BBDD_Unificada\\DatasetCompletoFemenino2.xlsx", index=False)
