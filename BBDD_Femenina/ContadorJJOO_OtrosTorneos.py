import pandas as pd
import unicodedata

# --- Función para normalizar nombres ---
def normalizar(nombre):
    if isinstance(nombre, str):
        nombre = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode('utf-8')
        return nombre.lower().replace(".", "").strip()
    return ""

# --- Cargar archivos ---
df_jugadores = pd.read_excel("jugadoras.xlsx")
df_torneos = pd.read_csv("torneos.csv", sep=';')

# --- Normalizar nombres ---
df_jugadores["nombre_normalizado"] = df_jugadores["Nombre"].apply(normalizar)
df_torneos["jugador_normalizado"] = df_torneos["Jugadora"].apply(normalizar)

# --- Juegos Olimpicos: Tour == IGF ---
olimpicos = df_torneos[df_torneos["Tour"] == "IGF"] \
    .drop_duplicates(subset=["jugador_normalizado"]) \
    .assign(Juegos_Olimpicos=1)[["jugador_normalizado", "Juegos_Olimpicos"]]

# --- Nº Otros Torneos: excluir LPGA, IGF y los que empiezan por "Previous"
otros_torneos = df_torneos[
    ~df_torneos["Tour"].isin(["LPGA", "IGF"]) &
    ~df_torneos["Tour"].str.startswith("Previous", na=False)
].groupby("jugador_normalizado").size().reset_index(name="Nº Otros Torneos")

# --- Nº LPGA ---
pgat_torneos = df_torneos[df_torneos["Tour"] == "LPGA"] \
    .groupby("jugador_normalizado").size().reset_index(name="Nº PGAT")

# --- Total Torneos (todos los tours) ---
total_torneos = df_torneos.groupby("jugador_normalizado").size().reset_index(name="Total Torneos")

# --- Unir todo al archivo de jugadores ---
df_final = df_jugadores.merge(olimpicos, left_on="nombre_normalizado", right_on="jugador_normalizado", how="left")
df_final.drop(columns=["jugador_normalizado"], inplace=True, errors="ignore")

df_final = df_final.merge(otros_torneos, left_on="nombre_normalizado", right_on="jugador_normalizado", how="left")
df_final.drop(columns=["jugador_normalizado"], inplace=True, errors="ignore")

df_final = df_final.merge(pgat_torneos, left_on="nombre_normalizado", right_on="jugador_normalizado", how="left")
df_final.drop(columns=["jugador_normalizado"], inplace=True, errors="ignore")

df_final = df_final.merge(total_torneos, left_on="nombre_normalizado", right_on="jugador_normalizado", how="left")
df_final.drop(columns=["jugador_normalizado"], inplace=True, errors="ignore")


# Rellenar valores
if "Juegos_Olimpicos" in df_final.columns:
    df_final["Juegos_Olimpicos"] = df_final["Juegos_Olimpicos"].fillna(0).astype(int)
else:
    df_final["Juegos_Olimpicos"] = 0

if "Nº Otros Torneos" in df_final.columns:
    df_final["Nº Otros Torneos"] = df_final["Nº Otros Torneos"].fillna(0).astype(int)
else:
    df_final["Nº Otros Torneos"] = 0

if "Nº PGAT" in df_final.columns:
    df_final["Nº PGAT"] = df_final["Nº PGAT"].fillna(0).astype(int)
else:
    df_final["Nº PGAT"] = 0

if "Total Torneos" in df_final.columns:
    df_final["Total Torneos"] = df_final["Total Torneos"].fillna(0).astype(int)
else:
    df_final["Total Torneos"] = 0


# Eliminar columna conflictiva
df_final.drop(columns=["jugador_normalizado"], inplace=True, errors="ignore")

# Guardar resultado
df_final.to_excel("jugadores_con_torneos_completo2.xlsx", index=False)
print("Archivo generado: jugadores_con_torneos_completo.xlsx")

