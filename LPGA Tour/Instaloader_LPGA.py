import csv
import time
import random
from instaloader import Instaloader, Profile
from instaloader.exceptions import *
from datetime import datetime
from datetime import timedelta
from itertools import dropwhile, takewhile
from os import listdir, mkdir
from instaloader.instaloadercontext import default_user_agent
import requests

ruta_archivo_origen = r'C:\\NAS_PAU\\TFG\\LPGA\\BuscarInstagram.csv'
ruta_archivo_destino = r'C:\\NAS_PAU\\TFG\\LPGA\\Instagram\\insta_posts.csv'

columns = ['player', 'username', 'num', 'post', 'shortcode', 'fecha', 'hora', 'n_carrusel', 'n_fotos', 'n_videos', 'visualizaciones_video', 'likes', 'comentarios', 'texto',
           'hashtags', 'is_sponsored', 'sponsor_users', 'tagged_users', 'mentions']

def simular_navegacion(session: requests.Session, username: str):
    """Simula navegación aleatoria en Instagram."""
    urls = [
        "https://www.instagram.com/",
        "https://www.instagram.com/explore/",
        f"https://www.instagram.com/{username}/",
        "https://www.instagram.com/accounts/edit/",
        "https://www.instagram.com/reels/",
        "https://www.instagram.com/explore/people/",
        "https://www.instagram.com/explore/tags/golf/",
        "https://www.instagram.com/explore/tags/sports/",
        "https://www.instagram.com/direct/inbox/",
        "https://www.instagram.com/accounts/activity/",
        "https://www.instagram.com/stories/highlights/",
        f"https://www.instagram.com/stories/{username}/",
        f"https://www.instagram.com/{username}/saved/",
        f"https://www.instagram.com/{username}/tagged/",
        f"https://www.instagram.com/{username}/followers/",
        f"https://www.instagram.com/{username}/following/",
        "https://www.instagram.com/reels/audio/",
        "https://www.instagram.com/reels/trending/",
        "https://www.instagram.com/creatorstudio/",
    ]

    url = random.choice(urls)
    print(f"Simulando navegación a {url}")
    try:
        response = session.get(url)
        if response.status_code == 200:
            print("Navegación simulada OK.")
        else:
            print(f"Respuesta inesperada: {response.status_code}")
    except Exception as e:
        print(f"Error simulando navegación: {e}")

    time.sleep(random.uniform(10, 20))  # Pausa aleatoria


def descarga_posts_entre_fechas_incluidas(str_profile, dt_fecha_inicio, dt_fecha_final, str_directorio, user, password):
    L = Instaloader(compress_json=False, save_metadata=False)
    loader.context._session.headers['User-Agent'] = default_user_agent()

    try:
        L.load_session_from_file(user)
        print('Sesión cargada correctamente')
    except:
        print('La sesión no se ha podido cargar. Iniciando sesión de nuevo')
        L.login(user, password)
        L.save_session_to_file(user)
        print('Sesión iniciada con éxito')

    profile = Profile.from_username(L.context, str_profile)
    posts = profile.get_posts()

    lista_filas = []
    n = 0
    publicaciones_antiguas = 0  # Contador para las publicaciones más antiguas

    session = L.context._session 

    # Iteramos por las publicaciones
    for post in posts:
        # Si la fecha de la publicación es anterior a la fecha de inicio, la consideramos antigua
        if post.date < dt_fecha_inicio:
            publicaciones_antiguas += 1
        
        # Si ya encontramos 3 publicaciones antiguas, detenemos la descarga
        if publicaciones_antiguas >= 4:
            try:
                L.download_profilepic(profile)
                print('Foto de perfil descargada con éxito')
            except Exception as e:
                print(f"Error al procesar la foto de perfil: {e}")
            print("Se han encontrado 4 publicaciones más antiguas. Deteniendo el proceso.")
            break
        
        # Procesamos las publicaciones dentro del rango de fechas
        if dt_fecha_inicio <= post.date <= dt_fecha_final:
            try: 
                sleep_time = random.uniform(5, 10)  # espera entre 5 y 15 segundos
                print(f"Esperando {sleep_time:.2f} segundos para no llamar la atención...")
                time.sleep(sleep_time)
                L.download_post(post, str_directorio)
            except InstaloaderException:
                print(f"Error al descargar el post: {post}")

            n += 1

            if n % 5 == 0:
                simular_navegacion(session, str_profile)

            # Procesamos los detalles de la publicación
            n_fotos = 0
            n_videos = 0
            n_carrusel = 0
            

            if post.typename == 'GraphSidecar':
                n_carrusel = 1
                for node in post.get_sidecar_nodes():
                    if node.is_video:
                        n_videos += 1
                    else:
                        n_fotos += 1
            elif post.typename == 'GraphVideo':
                n_videos = 1
            elif post.typename == 'GraphImage':
                n_fotos = 1

            fila = {
                'player': profile.full_name,
                'username': post.owner_username,
                'num': 0,
                'post': post.date.strftime('%Y-%m-%d_%H-%M-%S_UTC'),
                'shortcode': post.shortcode,
                'fecha': post.date.strftime('%Y-%m-%d'),
                'hora': post.date.strftime('%H:%M:%S'),
                'n_carrusel': n_carrusel,
                'n_fotos': n_fotos,
                'n_videos': n_videos,
                'visualizaciones_video': post.video_view_count,
                'likes': post.likes,
                'comentarios': 0,
                'texto': post.caption.replace('\n', ' ').replace('\r', ' ') if post.caption else "",
                'hashtags': '; '.join(set(post.caption_hashtags)) if post.caption else "",
                'is_sponsored': False,
                'sponsor_users': [],
                'tagged_users': [],
                'mentions': []
            }

            try:
                fila['comentarios'] = post.comments
            except ConnectionException as e:
                print(f"[{user}] Error al obtener comentarios: {e}")
                fila['comentarios'] = 'Error'

            try:
                fila['is_sponsored'] = post.is_sponsored
                if fila['is_sponsored']:
                    fila['sponsor_users'] = '; '.join(user.username for user in (post.sponsor_users or []))
            except Exception as e:
                print(f"Error al procesar patrocinio del post: {e}")

            try:
                fila['tagged_users'] = []
                if post.tagged_users:
                    for user in post.tagged_users:
                        if hasattr(user, 'username'):
                            fila['tagged_users'].append(user.username)
                        else:
                            fila['tagged_users'].append(str(user))
            except Exception as e:
                print(f"Error al obtener usuarios etiquetados: {e}")
                fila['tagged_users'] = []

            try:
                fila['mentions'] = post.caption_mentions if post.caption_mentions else []
            except Exception as e:
                print(f"Error al obtener menciones del texto: {e}")
                fila['mentions'] = []

            lista_filas.append(fila)

            if n % 50 == 0:
                print(f'{"-"*10} DURMIENDO 15 SEGUNDOS {"-"*10}')
                time.sleep(15)

    # Reordenamos las filas
    for i, fila in enumerate(reversed(lista_filas)):
        fila['num'] = i + 1

    resumen_path = f"{str_directorio}/{str_profile}_resumen.csv"
    with open(resumen_path, 'w', encoding='utf-8', newline='') as archivo:
        writer = csv.DictWriter(archivo, fieldnames=columns, delimiter=',', lineterminator='\n')
        writer.writeheader()
        writer.writerows(reversed(lista_filas))

    return n, profile.followers, profile.mediacount, profile.biography, profile.biography_hashtags, profile.biography_mentions, lista_filas



# FECHAS A DESCARGAR
INICIO = datetime(2024, 1, 1)
FINAL = datetime(2024, 12, 31)

# LOGIN
user = 'zaqvho'
#user = 'pgf220399'
#user = 'pauupv1'
#user = 'federer2203'
password = 'Qwerty88!'
loader = Instaloader(compress_json=False, save_metadata=False)
loader.context._session.headers['User-Agent'] = default_user_agent()

try:
    loader.load_session_from_file(user)
    print('Sesión cargada correctamente')
except:
    print('La sesión no se ha podido cargar. Iniciando sesión de nuevo')
    loader.login(user, password)
    loader.save_session_to_file(user)
    print('Sesión iniciada con éxito')
min_point = 230
max_point = 240

checkpoint = 0
with open(ruta_archivo_origen, 'r', newline='', encoding='utf-8') as archivo:
    lector_csv = csv.DictReader(archivo, delimiter=';')
    lista_jugadores = list(lector_csv)
columnas_origen = lector_csv.fieldnames

with open(ruta_archivo_destino, 'r', newline='', encoding='utf-8') as destino_csv:
    reader_csv = csv.DictReader(destino_csv, delimiter=',')
    for _ in reader_csv:
        checkpoint += 1

with open(ruta_archivo_destino, 'a', newline='', encoding='utf-8') as destino_csv:
    writer = csv.DictWriter(destino_csv, fieldnames=columns, delimiter=',')
    counter = min_point
    with open(ruta_archivo_origen, 'r', newline='', encoding='utf-8') as archivo:
        lector_csv = csv.DictReader(archivo, delimiter=';')
        for _ in range(min_point):
            next(lector_csv)
        while counter < max_point:
            for fila in lector_csv:
                if 'instagram.com' in fila['Instagram']:
                    counter += 1
                    player_name = fila['Jugadora']
                    str_profile = fila['Instagram'].split("instagram.com/")[1].split("/")[0].split("?")[0]

                    print(player_name)
                    print(str_profile)

                    if str_profile not in listdir('.'):
                        mkdir(str_profile)

                    print(f'Descargando posts en el directorio {str_profile}...')
                    time.sleep(random.uniform(5, 30))

                    session = loader.context._session
                    simular_navegacion(session, str_profile)

                    n_posts, seguidores, n_total_posts, biografia, hastags, menciones, lista_filas = descarga_posts_entre_fechas_incluidas(
                        str_profile, INICIO, FINAL, str_profile, user, password)

                    for fila_post in lista_filas:
                        writer.writerow(fila_post)

                    for jugador in lista_jugadores:
                        if jugador['Instagram'] == fila['Instagram']:
                            jugador['Descargado'] = str(n_posts)
                            jugador['Seguidores'] = str(seguidores)
                            jugador['Posts'] = str(n_total_posts)
                            jugador['Biografia'] = str(biografia)
                            jugador['Hastags_Biografia'] = str(hastags)
                            jugador['Meciones_Biografia'] = str(menciones)
                            break
                    with open(ruta_archivo_origen, 'w', newline='', encoding='utf-8') as archivo:
                        escritor_csv = csv.DictWriter(archivo, fieldnames=columnas_origen, delimiter=';')
                        escritor_csv.writeheader()
                        escritor_csv.writerows(lista_jugadores)            
                    print(f'OPERACIÓN FINALIZADA\n  Se han descargado {n_posts} posts de {str_profile}')
                    restantes = max_point - counter
                    print(f"Quedan {restantes} jugadores por procesar.")

                if counter >= max_point:
                    break

        print('Descarga de posts de todos los jugadores de la tanda finalizada')

print("Cuentas de Instagram obtenidas:", max_point - min_point)