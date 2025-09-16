import instaloader
from instaloader import Profile, InstaloaderException
import pandas as pd
import os
import time
import csv
from datetime import datetime, timedelta
from itertools import dropwhile, takewhile

# === CONFIGURACIÓN ===
usuario = 'jugadoresgolf22'
clave = 'Qwerty88!'
archivo_excel = 'C:\\NAS_PAU\\TFG\\PGA\\PGACompletoDepurado.csv'
archivo_csv = 'C:\\NAS_PAU\\TFG\\PGA\\insta_posts.csv'

inicio = datetime.strptime('2024-01-01', '%Y-%m-%d')
final = datetime.strptime('2024-12-31', '%Y-%m-%d')

FILA_INICIO = 1
FILA_FIN = 1000

carpeta_destino = os.path.dirname(archivo_csv)
os.makedirs(carpeta_destino, exist_ok=True)

# === INSTALOADER ===
L = instaloader.Instaloader(
    download_comments=True,
    save_metadata=False,
    post_metadata_txt_pattern='',
    download_video_thumbnails=True
)

# === AUTENTICACIÓN ROBUSTA ===
try:
    L.load_session_from_file(usuario)
    test_profile = Profile.from_username(L.context, 'instagram')
    print("✅ Sesión cargada correctamente.")
except Exception:
    print("🔐 Sesión no válida o no existente. Iniciando sesión...")
    L.login(usuario, clave)
    L.save_session_to_file()
    print("✅ Sesión iniciada y guardada.")

# === FUNCIÓN PARA DESCARGAR POSTS ===
def descarga_posts(cuenta, inicio, final, carpeta_destino):
    resumen_csv = []
    try:
        profile = Profile.from_username(L.context, cuenta)
        posts = profile.get_posts()
    except Exception as e:
        print(f"❌ No se pudo acceder a @{cuenta}: {e}")
        return 0, 0

    destino_cuenta = os.path.join(carpeta_destino, cuenta)
    os.makedirs(destino_cuenta, exist_ok=True)

    for post in takewhile(lambda p: p.date > inicio,
                          dropwhile(lambda p: p.date > final + timedelta(days=1), posts)):
        try:
            L.download_post(post, destino_cuenta)
        except InstaloaderException as e:
            print(f"⚠️ Error descargando post: {e}")
            continue

        # Comentarios
        try:
            comentarios_texto = [f"[{c.owner.username}]: {c.text.replace('\n', ' ').strip()}" for c in post.get_comments()]
            comentarios_concat = ' || '.join(comentarios_texto)
        except Exception as e:
            print(f"⚠️ No se pudieron obtener los comentarios de @{cuenta} - {post.shortcode}: {e}")
            comentarios_concat = 'ERROR'

        fila = {
            'usuario': cuenta,
            'num': 0,
            'post': post.date.strftime('%Y-%m-%d_%H-%M-%S_UTC'),
            'shortcode': post.shortcode,
            'fecha': (post.date + timedelta(hours=1)).strftime('%Y-%m-%d'),
            'hora': (post.date + timedelta(hours=1)).strftime('%H:%M:%S'),
            'video': int(post.is_video),
            'likes': post.likes,
            'comentarios': post.comments,
            'texto': post.caption.replace('\n', ' ').replace('\r', ' ') if post.caption else '',
            'hashtags': '; '.join(set(post.caption_hashtags)) if post.caption else '',
            'geotags': post.location.name if post.location else 'Sin localización',
            'is_sponsored': getattr(post, 'is_sponsored', False),
            'sponsor_users': ', '.join([s.username for s in getattr(post, 'sponsor_users', [])]) if getattr(post, 'is_sponsored', False) else '',
            'comentarios_texto': comentarios_concat,
            'seguidores': profile.followers
        }

        resumen_csv.append(fila)

    for i, fila in enumerate(reversed(resumen_csv)):
        fila['num'] = i + 1

    return resumen_csv


# === MAIN ===
if __name__ == '__main__':
    df = pd.read_csv(archivo_excel, encoding='latin1', sep=';')

    if 'Instagram' not in df.columns:
        raise ValueError("⚠️ La columna 'Instagram' no existe en el Excel")

    total_global = 0
    total_cuentas = 0
    resumen_global = []

    for idx, row in df.iterrows():
        excel_index = idx + 1
        if excel_index < FILA_INICIO or excel_index > FILA_FIN:
            continue

        if not isinstance(row['Instagram'], str) or 'instagram.com/' not in row['Instagram']:
            continue

        cuenta = row['Instagram'].split("instagram.com/")[1].split("/")[0]
        if not cuenta or cuenta == 'nan':
            continue

        total_cuentas += 1
        print(f"\n📥 [{excel_index}] Procesando @{cuenta}...")

        resumen_cuenta = descarga_posts(cuenta, inicio, final, carpeta_destino)
        total_publicaciones = len(resumen_cuenta)
        print(f"✅ @{cuenta}: {total_publicaciones} publicaciones descargadas")

        resumen_global.extend(resumen_cuenta)
        total_global += total_publicaciones

        time.sleep(10)  # PAUSA MÁS LARGA ENTRE CUENTAS

    # Guardar resumen global
    if resumen_global:
        with open(archivo_csv, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(resumen_global[0].keys()), delimiter='\t')
            writer.writeheader()
            writer.writerows(resumen_global)

    print(f"\n🎯 Finalizado. Total cuentas: {total_cuentas} | Total publicaciones: {total_global}")
