import pandas as pd

# RUTAS DE ARCHIVOS
file_pga = "C:\\NAS_PAU\\TFG\\PGA\\PGACompletoDepurado.csv"
file_liv = "C:\\NAS_PAU\\TFG\\LIV\\LIVinformacionjugadores2024.csv"

# CARGA DE DATOS CON FORMATO ROBUSTO
df_pga = pd.read_csv(file_pga, sep=";", quoting=1, encoding='utf-8', engine='python')
df_liv = pd.read_csv(file_liv, sep=";", quoting=1, encoding='utf-8', engine='python')

# RENOMBRAR COLUMNAS PARA ESTANDARIZAR
df_pga = df_pga.rename(columns={
    "Jugador": "Nombre",
    "AÃ±o profesional": "Inicio Profesional",
    "Dinero oficial PGA 2024": "Dinero 2024",
    "Lugar nacimiento": "País",
    "Meciones_Biografia": "Menciones_Biografia"
})
df_liv = df_liv.rename(columns={
    "Meciones_Biografia": "Menciones_Biografia"
})

# AÑADIR COLUMNA TOUR
df_pga["Tour"] = "PGA"
df_liv["Tour"] = "LIV"

# EXTRAER USERNAME DE INSTAGRAM
df_pga["Username"] = df_pga["Instagram"].str.extract(r"instagram\.com/([^/]+)/?")
df_liv["Username"] = df_liv["Instagram"].str.extract(r"instagram\.com/([^/]+)/?")

# DEFINIR COLUMNAS FINALES EN ORDEN
columnas_finales = [
    "Nombre", "Edad", "Username", "Inicio Profesional", "Dinero 2024", "País",
    "Posición OWGR", "Tour", "NºTorneos", "NºMajors",
    "Instagram", "Seguidores", "Posts", "Descargado", "Biografia",
    "Hastags_Biografia", "Menciones_Biografia"
]

# ASEGURAR PRESENCIA DE TODAS LAS COLUMNAS
for col in columnas_finales:
    if col not in df_pga.columns:
        df_pga[col] = ""
    if col not in df_liv.columns:
        df_liv[col] = ""

# REORDENAR Y UNIR
df_pga = df_pga[columnas_finales]
df_liv = df_liv[columnas_finales]
df_total = pd.concat([df_pga, df_liv], ignore_index=True)

# EXPORTAR A EXCEL
df_total.to_excel("C:\\NAS_PAU\\TFG\\jugadores_LIV_PGA_unificado.xlsx", index=False)

