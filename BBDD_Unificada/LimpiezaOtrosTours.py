import pandas as pd
import ast 

# Cargar el archivo
df = pd.read_excel("jugadores_LIV_PGA_unificado.xlsx")

# Función para limpiar la lista
def limpiar_tours(tours):
    try:
        lista = ast.literal_eval(tours)
        lista_filtrada = [t for t in lista if not t.startswith("Previous") and t != "PGAT"]
        return ", ".join(lista_filtrada)
    except:
        return ""

# Aplicar la limpieza
df["Otros Tours Limpios"] = df["Otros Tours Jugados"].apply(limpiar_tours)

# Guardar
df.to_excel("jugadores_tours_limpios.xlsx", index=False)


