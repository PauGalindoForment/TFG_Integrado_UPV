import pandas as pd

rutas_csv_1000 = [
    "RolexRankingtorneosjugadora1-500.csv",
    "RolexRankingtorneosjugadora501-1000.csv"
]

# Leer todos los archivos correctamente usando separador ";"
df_1000 = pd.concat(
    [pd.read_csv(ruta, encoding='latin1', sep=';') for ruta in rutas_csv_1000],
    ignore_index=True
)

# Ordenar si existen las columnas necesarias
if 'Jugador' in df_1000.columns and 'Semana' in df_1000.columns:
    df_1000.sort_values(by=['Jugadora', 'Año', 'Semana'], inplace=True)

# Guardar a Excel
ruta_1000 = "Rolex_torneos_hasta_1000.xlsx"
df_1000.to_excel(ruta_1000, index=False)
