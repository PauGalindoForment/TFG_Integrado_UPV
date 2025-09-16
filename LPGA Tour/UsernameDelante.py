import os

# Ruta principal donde están todas las carpetas de los usuarios
RUTA_PRINCIPAL = 'C:\\NAS_PAU\\TFG\\LPGA\\Instagram'

SUBCARPETAS = ['fotos', 'videos', 'textos']

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
                        # Evita renombrar si ya está bien puesto
                        if not archivo.startswith(f"{usuario}_"):
                            os.rename(ruta_archivo, ruta_nueva)
                            print(f"{archivo} -> {nuevo_nombre}")

print("Todos los archivos tienen el username delante.")