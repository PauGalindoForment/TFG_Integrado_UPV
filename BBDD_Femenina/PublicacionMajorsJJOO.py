import pandas as pd

# Cargar los archivos
df_posts = pd.read_excel('C:\\NAS_PAU\\TFG\\BBDD_Femenino\\DatasetCompletoFemenino.xlsx')       
df_torneos = pd.read_csv('C:\\NAS_PAU\\TFG\\BBDD_Femenino\\torneos.csv', sep=';')  

# Asegurar formato de fecha
df_posts['fecha'] = pd.to_datetime(df_posts['fecha'])

# Definir fechas de las semanas de majors
majors = {
    'The Chevron Championship': ('2024-04-16', '2024-04-23'),
    "U.S. Women's Open presented by Ally": ('2024-05-28', '2024-06-04'),
    "KPMG Women's PGA Championship": ('2024-06-18', '2024-06-25'),
    'The Amundi Evian Championship': ('2024-07-09', '2024-07-16'),
    "AIG Women's Open": ('2024-08-20', '2024-08-27'),
    "2024 Olympics Golf - Women's Golf": ('2024-08-07', '2024-08-12')
}

# 4. Mapear nombres de columnas a crear
col_map = {
    'The Chevron Championship': 'Chevron',
    "U.S. Women's Open presented by Ally": 'US Open',
    "KPMG Women's PGA Championship": 'KPMG',
    'The Amundi Evian Championship': 'Amundi',
    "AIG Women's Open":"AIG",
    "2024 Olympics Golf - Women's Golf":"OGC"
}

# 5. Inicializar las nuevas columnas con 0
for col in col_map.values():
    df_posts[col] = 0

# 6. Para cada major, marcar con 1 si participó y publicó durante el torneo
for torneo, (start, end) in majors.items():
    participantes = df_torneos[df_torneos['Evento'] == torneo]['Jugadora'].unique()
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
df_posts.to_excel('C:/NAS_PAU/TFG/BBDD_Femenino/DatasetCompletoFemenino.xlsx', index=False)

