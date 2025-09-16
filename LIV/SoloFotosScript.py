import os
import shutil

# Cambia a la ruta donde tienes todas las carpetas de usuarios
RUTA_USUARIOS = 'C:\\NAS_PAU\\TFG\\LIV\\Instagram'       
RUTA_DESTINO = 'C:\\NAS_PAU\\TFG\\LIV\\Instagram\\Solo_fotos'                 

# Creamos la carpeta destino si no existe
if not os.path.exists(RUTA_DESTINO):
    os.makedirs(RUTA_DESTINO)

# Recorremos cada carpeta de usuario
for usuario in os.listdir(RUTA_USUARIOS):
    ruta_usuario = os.path.join(RUTA_USUARIOS, usuario)
    if os.path.isdir(ruta_usuario):
        ruta_fotos = os.path.join(ruta_usuario, "fotos")
        if os.path.exists(ruta_fotos):
            destino_usuario = os.path.join(RUTA_DESTINO, usuario)
            # Copia toda la carpeta "fotos" y su contenido
            shutil.copytree(ruta_fotos, os.path.join(destino_usuario, "fotos"))
            print(f'Copiado: {usuario}/fotos')

print("Ahora tienes una carpeta con solo las fotos y la misma estructura por usuario.")
