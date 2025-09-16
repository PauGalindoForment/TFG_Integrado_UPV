import os

# Ruta principal donde están todas las carpetas de los usuarios
RUTA_PRINCIPAL = 'C:\\NAS_PAU\\TFG\\PGA\\Instagram'

# Subcarpetas por tipo de archivo
SUBCARPETAS = ['fotos', 'videos', 'textos']

# Recorre cada carpeta de usuario
for usuario in os.listdir(RUTA_PRINCIPAL):
    ruta_usuario = os.path.join(RUTA_PRINCIPAL, usuario)
    if os.path.isdir(ruta_usuario):
        for sub in SUBCARPETAS:
            ruta_sub = os.path.join(ruta_usuario, sub)
            if os.path.isdir(ruta_sub):
                for archivo in os.listdir(ruta_sub):
                    ruta_archivo = os.path.join(ruta_sub, archivo)
                    if os.path.isfile(ruta_archivo):
                        nuevo_nombre = f"{usuario}_{archivo}"
                        ruta_nueva = os.path.join(ruta_sub, nuevo_nombre)
                        # Solo renombrar si aún no está correctamente nombrado
                        if not archivo.startswith(f"{usuario}_"):
                            # Si ya existe, será sobrescrito
                            if os.path.exists(ruta_nueva):
                                os.remove(ruta_nueva)
                            os.rename(ruta_archivo, ruta_nueva)
                            print(f"{archivo} -> {nuevo_nombre}")

print("Todos los archivos renombrados con el username delante (sobrescribiendo si es necesario).")

