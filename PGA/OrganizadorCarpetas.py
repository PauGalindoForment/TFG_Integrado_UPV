import os
import shutil

# Ruta principal donde están todas las carpetas de los usuarios
RUTA_PRINCIPAL = 'C:\\NAS_PAU\\TFG\\PGA\\Instagram'

# Extensiones y sus subcarpetas correspondientes
TIPOS = {
    '.jpg': 'fotos',
    '.jpeg': 'fotos',
    '.mp4': 'videos',
    '.txt': 'textos'
}

# Recorremos cada carpeta de usuario
for usuario in os.listdir(RUTA_PRINCIPAL):
    ruta_usuario = os.path.join(RUTA_PRINCIPAL, usuario)
    if os.path.isdir(ruta_usuario):
        # Crear subcarpetas si no existen
        for carpeta in set(TIPOS.values()):
            ruta_sub = os.path.join(ruta_usuario, carpeta)
            os.makedirs(ruta_sub, exist_ok=True)
        
        # Procesar archivos sueltos
        for archivo in os.listdir(ruta_usuario):
            ruta_archivo = os.path.join(ruta_usuario, archivo)
            if os.path.isfile(ruta_archivo):
                ext = os.path.splitext(archivo)[1].lower()
                if ext in TIPOS:
                    destino = os.path.join(ruta_usuario, TIPOS[ext], archivo)
                    if os.path.exists(destino):
                        os.remove(ruta_archivo)
                        print(f'Duplicado eliminado: {archivo}')
                    else:
                        shutil.move(ruta_archivo, destino)
                        print(f'Movido: {archivo} -> {TIPOS[ext]}')

print('Organización y limpieza completadas.')
