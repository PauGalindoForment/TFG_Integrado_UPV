import os
import pandas as pd
import unicodedata

# Rutas locales
excel_path = 'C:\\NAS_PAU\\TFG\\LIV\\NombreUsername.xlsx'
carpeta_fotos = 'C:\\NAS_PAU\\TFG\\LIV\\FotosPerfil'

# Función para normalizar texto (minúsculas, sin tildes, sin espacios)
def normalizar(texto):
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    texto = texto.replace(' ', '')
    return texto

# Leer el Excel
df = pd.read_excel(excel_path, sheet_name='Hoja1')

# Filtrar filas con datos válidos
df = df[df['Instagram'].notnull()]
df = df[~df['Instagram'].str.lower().str.contains('no tiene instagram')]

# ✅ Eliminar parámetros tipo ?hl=en de toda la columna
df['Instagram'] = df['Instagram'].str.split('?').str[0]

# ✅ Extraer username desde la URL limpia
df['username'] = df['Instagram'].apply(
    lambda url: url.rstrip('/').split('/')[-1] if isinstance(url, str) else ''
)

# Filtrar filas con username válido
df = df[df['username'].str.strip() != '']

# Crear diccionario: {nombre_normalizado: username}
mapa_nombre_a_username = {
    normalizar(nombre): username for nombre, username in zip(df['Nombre'], df['username'])
}

# Renombrar los archivos de imagen
for archivo in os.listdir(carpeta_fotos):
    if archivo.lower().endswith('.jpg'):
        nombre_base = os.path.splitext(archivo)[0]
        nombre_normalizado = normalizar(nombre_base)

        if nombre_normalizado in mapa_nombre_a_username:
            username = mapa_nombre_a_username[nombre_normalizado]
            ruta_vieja = os.path.join(carpeta_fotos, archivo)
            ruta_nueva = os.path.join(carpeta_fotos, f"{username}.jpg")

            if os.path.exists(ruta_nueva):
                print(f"⚠️ Ya existe: {ruta_nueva} — no se renombra {archivo}")
            else:
                os.rename(ruta_vieja, ruta_nueva)
                print(f"✅ Renombrado: {archivo} → {username}.jpg")
        else:
            print(f"⚠️ No encontrado en Excel: {archivo}")
