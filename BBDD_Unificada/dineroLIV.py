import pandas as pd

archivo_destino = "C:\\NAS_PAU\\TFG\\BBDD_Unificada\\Jugadores_PGA_LIV_Unificado.xlsx"
df_destino = pd.read_excel(archivo_destino)
archivo_fuente = "C:\\NAS_PAU\\TFG\\LIV\\liv_2024_ganancias_torneos.csv"
df_fuente = pd.read_csv(archivo_fuente, sep=';')

# Normalizar nombres para hacer el cruce
df_destino["nombre_lower"] = df_destino["Nombre"].str.lower().str.strip()
df_fuente["nombre_lower"] = df_fuente["Jugador"].str.lower().str.strip()

# Crear diccionarios: nombre dinero / torneos
ganancias_dict = df_fuente.set_index("nombre_lower")["Total ganado"].to_dict()
torneos_dict = df_fuente.set_index("nombre_lower")["Torneos jugados"].to_dict()

# Actualizar columnas solo si hay match
df_destino["Dinero 2024"] = df_destino.apply(
    lambda row: ganancias_dict[row["nombre_lower"]] if row["nombre_lower"] in ganancias_dict else row["Dinero 2024"],
    axis=1
)

df_destino["Nº Torneos LIV/PGA"] = df_destino.apply(
    lambda row: torneos_dict[row["nombre_lower"]] if row["nombre_lower"] in torneos_dict else row["Nº Torneos LIV/PGA"],
    axis=1
)

# Mostrar jugadores del CSV que no hicieron match
nombres_destino = set(df_destino["nombre_lower"])
nombres_fuente = set(df_fuente["nombre_lower"])
sobran_en_csv = nombres_fuente - nombres_destino

print("Archivo actualizado.")
if sobran_en_csv:
    print("\nJugadores del CSV que NO están en el Excel:")
    for nombre in sorted(sobran_en_csv):
        original = df_fuente.loc[df_fuente["nombre_lower"] == nombre, "Jugador"].values[0]
        print(" -", original)
else:
    print("\nTodos los jugadores del CSV hicieron match con el Excel.")

# Guardar archivo final
df_destino.drop(columns=["nombre_lower"], inplace=True)
salida = "C:\\NAS_PAU\\TFG\\BBDD_Unificada\\Jugadores_PGA_LIV_Unificado2.xlsx"
df_destino.to_excel(salida, index=False)
print(f"\nGuardado en: {salida}")

