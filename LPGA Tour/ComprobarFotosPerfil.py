import os

# === RUTAS ===
ruta_caras_perfil = "C:\\NAS_PAU\\TFG\\LPGA\\imagenes_jugadoras"
ruta_dataset = "G:\\La meva unitat\\TFG_Instagram\\LPGA"

# === 1. Extraer nombres de jugadores del dataset (por subcarpeta) ===
jugadores_dataset = set([
    nombre for nombre in os.listdir(ruta_dataset)
    if os.path.isdir(os.path.join(ruta_dataset, nombre))
])

# === 2. Extraer nombres de jugadores con imagen de perfil ===
jugadores_con_foto = set([
    os.path.splitext(nombre)[0]
    for nombre in os.listdir(ruta_caras_perfil)
    if nombre.lower().endswith(('.jpg', '.jpeg', '.png'))
])

# === 3. Comprobar faltantes y sobrantes ===
faltan_fotos = jugadores_dataset - jugadores_con_foto
fotos_sobrantes = jugadores_con_foto - jugadores_dataset

print("Jugadores SIN foto de perfil:")
print(sorted(faltan_fotos) if faltan_fotos else "Todos tienen foto de perfil.")

print("\nFotos de perfil que NO tienen carpeta de jugador:")
print(sorted(fotos_sobrantes) if fotos_sobrantes else "Todas las fotos tienen su carpeta.")
