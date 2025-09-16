import pandas as pd
from urllib.parse import urlparse
# Ruta del archivo Excel original
archivo_entrada = 'C:\\NAS_PAU\\TFG\\LPGA\\LPGA_informacionTOTAL.csv'  # Cambia este nombre si es necesario
archivo_salida = 'C:\\NAS_PAU\\TFG\\LPGA\\LPGA_informacionTOTAL.csv'

# Leer archivo
df = pd.read_csv(archivo_entrada, sep=';')

# Asumiendo que la columna se llama 'url'
def extraer_username(url):
    if not isinstance(url, str):
        return None
    path = urlparse(url).path  # Extrae la parte /username/
    username = path.strip('/').split('/')[0]  # Elimina / y extrae solo el nombre
    return username

df['username'] = df['Instagram'].apply(extraer_username)

# Guardar resultado en un nuevo archivo Excel
df.to_csv(archivo_salida, index=False, sep=';')

print("Usernames extraídos y guardados en:", archivo_salida)
