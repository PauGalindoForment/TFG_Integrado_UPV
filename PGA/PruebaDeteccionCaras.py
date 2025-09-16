import os
import cv2
from mtcnn import MTCNN
import pandas as pd

""" # 🔁 Para Google Colab: montar Google Drive
try:
    from google.colab import drive
    drive.mount('/content/drive')
    raiz_drive = '/content/drive/MyDrive'
except ImportError:
    print("Estás ejecutando esto en local.")
    raiz_drive = '.'  # Cambiar si tienes un path base en local """

# 📂 Rutas (ajusta según tu estructura)
directorio_raiz = 'C:\\NAS_PAU\\TFG\\PGA\\Instagram\\201-250\\scottie.scheffler' # Carpeta raíz con imágenes
db_path = 'C:\\NAS_PAU\\TFG\\PGA\\Instagram\\201-250\\scottie.scheffler\\CarasDetectadas'  # Donde guardar caras

# 🧠 Inicializa detector de rostros
detector_rostros = MTCNN()
os.makedirs(db_path, exist_ok=True)

# 📋 Lista para los resultados
face_data = []

# 🔁 Recorre imágenes del directorio
for subdir, _, files in os.walk(directorio_raiz):
    for nombre_imagen in files:
        if nombre_imagen.lower().endswith('.jpg') and 'UTC' in nombre_imagen:
            usuario = os.path.basename(subdir)
            img_path = os.path.join(subdir, nombre_imagen)

            # Carga y convierte a RGB
            imagen = cv2.imread(img_path)
            if imagen is None:
                print(f"⚠️ No se pudo leer la imagen: {img_path}")
                continue
            imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

            # 🧠 Detecta rostros
            rostros = detector_rostros.detect_faces(imagen_rgb)

            for i, rostro in enumerate(rostros):
                x, y, w, h = rostro['box']
                x, y = max(0, x), max(0, y)
                cara = imagen_rgb[y:y+h, x:x+w]

                # 📂 Crea carpeta del usuario
                carpeta_usuario = os.path.join(db_path, usuario)
                os.makedirs(carpeta_usuario, exist_ok=True)

                # 🏷️ Nombre único de la cara detectada
                face_id = f"{usuario}_{nombre_imagen.replace('.jpg', '')}_face{i}"
                ruta_cara = os.path.join(carpeta_usuario, face_id + '.jpg')

                # 💾 Guarda la cara
                cv2.imwrite(ruta_cara, cv2.cvtColor(cara, cv2.COLOR_RGB2BGR))

                # 📄 Guarda información
                face_data.append({
                    'username': usuario,
                    'original_image': nombre_imagen,
                    'image_path': img_path,
                    'face_id': face_id,
                    'face_path': ruta_cara
                })

                print(f"✅ Guardada cara de {usuario}: {ruta_cara}")

# 🗃️ Convierte a DataFrame y guarda en CSV
df_faces = pd.DataFrame(face_data)
csv_path = os.path.join('C:\\NAS_PAU\\TFG\\PGA\\Instagram\\201-250\\scottie.scheffler\\CarasDetectadas')
df_faces.to_csv(csv_path, index=False)
print(f"📁 CSV guardado en: {csv_path}")
