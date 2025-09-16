import os
import shutil

ORIGEN = 'C:\\NAS_PAU\\TFG\\PGA\\Instagram'
DESTINO = 'G:\\La meva unitat\\TFG_Instagram\\PGA'

for usuario in os.listdir(ORIGEN):
    ruta_usuario = os.path.join(ORIGEN, usuario)
    if os.path.isdir(ruta_usuario):
        print(f'🔍 Procesando usuario: {usuario}')
        for subcarpeta in ['fotos', 'textos']:
            origen_sub = os.path.join(ruta_usuario, subcarpeta)
            if os.path.exists(origen_sub):
                destino_usuario = os.path.join(DESTINO, usuario, subcarpeta)
                os.makedirs(destino_usuario, exist_ok=True)
                archivos = os.listdir(origen_sub)
                for archivo in archivos:
                    ruta_archivo = os.path.join(origen_sub, archivo)
                    destino_archivo = os.path.join(destino_usuario, archivo)
                    if not os.path.exists(destino_archivo):
                        shutil.copy2(ruta_archivo, destino_archivo)
                        print(f'   ✅ Copiado: {subcarpeta}/{archivo}')
                    else:
                        print(f'   ⚠️ Ya existe: {subcarpeta}/{archivo}')
        print('---')

print("✅ Copia completada. Solo fotos y textos están en la carpeta para Drive.")
