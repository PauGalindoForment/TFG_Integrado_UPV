import os
import pandas as pd

carpeta_usuarios = 'G:\\La meva unitat\\TFG_Instagram\\PGA'           
carpeta_imagenes = 'G:\\La meva unitat\\TFG_Instagram\\PGAla mtFotosPerfilWeb'    

# Obtener nombres de carpetas (usuarios)
usuarios = set(os.listdir(carpeta_usuarios))

# Obtener nombres base (sin extensión) de imágenes
imagenes = {
    os.path.splitext(nombre)[0]
    for nombre in os.listdir(carpeta_imagenes)
    if os.path.isfile(os.path.join(carpeta_imagenes, nombre))
}

# Comparaciones
faltan_imagenes = sorted(usuarios - imagenes)
sobran_imagenes = sorted(imagenes - usuarios)

# Crear DataFrame
df_resultado = pd.DataFrame({
    'Usuarios_sin_imagen': pd.Series(faltan_imagenes),
    'Imagenes_sin_usuario': pd.Series(sobran_imagenes)
})

# Guardar en Excel
archivo_salida = 'comparacion_fotos_vs_usuariosPGA.xlsx'
df_resultado.to_excel(archivo_salida, index=False)
print(f"Comparación completada. Archivo guardado como: {archivo_salida}")
