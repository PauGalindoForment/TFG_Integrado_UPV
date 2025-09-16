import pandas as pd

# Cargar los archivos
df_posts = pd.read_excel('C:\\NAS_PAU\\TFG\\BBDD_Unificada\\DatasetCompleto.xlsx')       
df_torneos = pd.read_excel('C:\\NAS_PAU\\TFG\\BBDD_Unificada\\torneosCOPIA.xlsx')  

# Asegurar formato de fecha
df_posts['fecha'] = pd.to_datetime(df_posts['fecha'])

# Definir fechas de las semanas de majors
majors = {
    # 'Masters Tournament': ('2024-04-09', '2024-04-16'),
    # 'U.S. PGA CHAMPIONSHIP': ('2024-05-14', '2024-05-21'),
    # 'U.S. OPEN': ('2024-06-11', '2024-06-18'),
    # 'The 152nd OPEN': ('2024-07-16', '2024-07-23'),
    "Olympic Men's Golf Competition": ('2024-07-30', '2024-08-06')

}

# 4. Mapear nombres de columnas a crear
col_map = {
    # 'Masters Tournament': 'Masters',
    # 'U.S. PGA CHAMPIONSHIP': 'PGA Championship',
    # 'U.S. OPEN': 'US Open',
    # 'The 152nd OPEN': 'The Open',
    "Olympic Men's Golf Competition":"OGC"
}

# 5. Inicializar las nuevas columnas con 0
for col in col_map.values():
    df_posts[col] = 0

# 6. Para cada major, marcar con 1 si participó y publicó durante el torneo
for torneo, (start, end) in majors.items():
    participantes = df_torneos[df_torneos['Evento'] == torneo]['Jugador'].unique()
    col = col_map[torneo]
    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)

    df_posts.loc[
        (df_posts['Nombre'].isin(participantes)) &
        (df_posts['fecha'] >= start_date) &
        (df_posts['fecha'] <= end_date),
        col
    ] = 1

# 7. Guardar si lo deseas
df_posts.to_excel('C:/NAS_PAU/TFG/BBDD_Unificada/DatasetCompleto.xlsx', index=False)

