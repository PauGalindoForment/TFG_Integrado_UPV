import pandas as pd

# Cargar archivo
df = pd.read_excel("C:\\NAS_PAU\\TFG\\BBDD_Unificada\\DatosPublicacionesPGALIV.xlsx")

# Asegúrate de reemplazar 'pais' por el nombre real de la columna que contiene los países
df['es_usa'] = df['País'].apply(lambda x: 1 if isinstance(x, str) and 'estados unidos' in x.lower() else 0)

# Guardar el resultado si quieres
df.to_excel("C:\\NAS_PAU\\TFG\\BBDD_Unificada\\DatosPublicacionesPGALIV.xlsx", index=False)

# Mostrar primeras filas
print(df[['País', 'es_usa']].head())
