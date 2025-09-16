import os
import shutil

# Ruta principal donde están todas las carpetas de los usuarios
RUTA_PRINCIPAL = 'C:\\NAS_PAU\\TFG\\LIV\\Instagram'  

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
        # Creamos subcarpetas si no existen
        for carpeta in set(TIPOS.values()):
            ruta_sub = os.path.join(ruta_usuario, carpeta)
            if not os.path.exists(ruta_sub):
                os.makedirs(ruta_sub)
        
        # Movemos archivos
        for archivo in os.listdir(ruta_usuario):
            ruta_archivo = os.path.join(ruta_usuario, archivo)
            if os.path.isfile(ruta_archivo):
                ext = os.path.splitext(archivo)[1].lower()
                if ext in TIPOS:
                    destino = os.path.join(ruta_usuario, TIPOS[ext], archivo)
                    shutil.move(ruta_archivo, destino)
                    print(f'Movido: {archivo} -> {TIPOS[ext]}')

print('Todos los archivos están organizados por tipo en cada carpeta de usuario.')
