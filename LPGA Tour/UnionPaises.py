import pandas as pd

# Cargar el archivo CSV con separador ;
df = pd.read_csv("LPGA_informacionTOTAL.csv", sep=';', engine='python')

# Función para clasificar el país
def clasificar_pais(row):
    if 'United States' in str(row['Pais_x']) or 'United States' in str(row['Pais_y']):
        return 'Estados Unidos'
    if 'USA' in str(row['Pais_x']) or 'USA' in str(row['Pais_y']):
        return 'Estados Unidos'
    return 'Otra'

# Aplicar la función y crear la nueva columna
df['Pais'] = df.apply(clasificar_pais, axis=1)

# Guardar el nuevo archivo (opcional)
df.to_excel("LPGA_informacionTOTAL.xlsx", index=False)
