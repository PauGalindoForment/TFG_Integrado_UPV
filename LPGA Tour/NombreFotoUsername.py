import os
import pandas as pd

# Ruta a la carpeta con las imágenes
carpeta = "C:\\NAS_PAU\\TFG\\LPGA\\imagenes_jugadoras"

# Ruta al Excel con columnas: archivo original y username
archivo_excel = "C:\\NAS_PAU\\TFG\\LPGA\\nombres_jugadoras.xlsx"

# Cargar Excel
df = pd.read_excel(archivo_excel)

# Recorrer cada fila y renombrar
for _, row in df.iterrows():
    nombre_base = os.path.splitext(row['archivo'])[0]  # Sin extensión
    username = row['username']
    
    if pd.isna(username) or not str(username).strip():
        continue  # Saltar si no hay username

    # Buscar si existe archivo .jpg o .png
    ruta_origen_jpg = os.path.join(carpeta, nombre_base + ".jpg")
    ruta_origen_png = os.path.join(carpeta, nombre_base + ".png")

    # Crear nuevo nombre con extensión que corresponda
    if os.path.exists(ruta_origen_jpg):
        ext = ".jpg"
        ruta_origen = ruta_origen_jpg
    elif os.path.exists(ruta_origen_png):
        ext = ".png"
        ruta_origen = ruta_origen_png
    else:
        print(f"No encontrado: {nombre_base}.jpg/.png")
        continue

    # Nuevo nombre con misma extensión
    nombre_nuevo = username.strip() + ext
    ruta_destino = os.path.join(carpeta, nombre_nuevo)

    # Renombrar si no existe el destino
    if not os.path.exists(ruta_destino):
        os.rename(ruta_origen, ruta_destino)
        print(f"Renombrado: {os.path.basename(ruta_origen)} → {nombre_nuevo}")
    else:
        print(f"Ya existe: {nombre_nuevo}, se omite.")

