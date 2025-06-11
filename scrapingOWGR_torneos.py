import csv
from os import path
import re
import time
import pandas as pd
import requests as req
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Ruta del archivo csv
csv_profiles = 'C:\\NAS_PAU\\TFG\\OWGR\\OWGRprofiles.csv'
csv_torneos = 'C:\\NAS_PAU\\TFG\\OWGR\\OWGRtorneosjugador3501-4000s.csv'
csv_jugador_foto = 'C:\\NAS_PAU\\TFG\\OWGR\\OWGRjugadorfoto3501-4000s.csv'
carpeta_img_perfil = 'C:\\NAS_PAU\\TFG\\OWGR\\FotosPerfil\\3501-4000'

# Opciones Chrome WebDriver
options = webdriver.ChromeOptions()
options.page_load_strategy = 'normal' 
options.add_argument("--headless")
driver = Chrome(options=options)
driver.implicitly_wait(5)

# Listas para almacenar datos
torneos = []
img_url = []
nombre_perf = []
best_posicion = []

# Controlar los jugadores que se procesarán por ejecución
perfiles = []
num_prev = 1
num_post = 500

# Leer perfiles desde el CSV
with open(csv_profiles, mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        perfiles.append(row[0])

print(perfiles)

# Procesar cada jugador
for perfil in perfiles[num_prev:num_post]:
    url_2024 = perfil + '?tab=events&year=2024'
    # Verificar si la página existe antes de abrirla en Selenium
    response = req.get(url_2024)

    if response.status_code != 200:
        print(f"Página no encontrada para {perfil}. El jugador ya no existe en OWGR.")
        nombre = perfil.split('/')[-1]  # Extraer el identificador del jugador de la URL
        torneos.append([nombre, "Perfil no encontrado", "", "", "", "", "", "", "", "", ""])
        continue  # Saltar al siguiente jugador
    driver.get(url_2024)
    time.sleep(1)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
    except TimeoutException:
        print(f"Tiempo de espera agotado para {perfil}. No se encontraron torneos.")

    # Obtener HTML
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Extraer información del jugador
    nombre = soup.find('div', {'class':'playerInfoView_player__name__mjkdj'}).text.strip()
    nombre_perf.append(nombre)

    # Extraer mejor posición OWGR
    mejor_posicion = soup.find_all('div', {'class':'playerStatisticsView_element__value__sHVly'})
    valor1 = valor2 = 0

    if len(mejor_posicion) > 1:
        valor1 = re.sub(r'[^0-9.-]', '', mejor_posicion[0].text.strip()) or "9999"
        valor2 = re.sub(r'[^0-9.-]', '', mejor_posicion[1].text.strip()) or "9999"
        valor1, valor2 = int(valor1), int(valor2)

    menor_valor = min(valor1, valor2)
    
    # Extraer imagen del jugador
    try:
        foto = soup.find('div', {'class': 'playerImage_image__1WZ59'})
        foto_jugador = foto.find('img', {'alt': nombre}).get('src')
        img_url.append(foto_jugador)
    except AttributeError:
        img_url.append("El jugador no tiene foto en el OWGR")
        foto_jugador = None

    print(nombre)
    print(f'Mejor posición OWGR: {menor_valor}')
    best_posicion.append(menor_valor)

    # Guardar imagen
    if foto_jugador:
        img_response = req.get(foto_jugador, stream=True)            
        file_path = path.join(carpeta_img_perfil, f"{nombre}.jpg")  
        with open(file_path, "wb") as file:
            for chunk in img_response.iter_content(1024):
                file.write(chunk)
        print(f"Imagen guardada en: {file_path}")

    # Extraer torneos
    filas = soup.find_all('tr')

    if not filas:
        print(f"No se encontraron torneos para {nombre} en 2024.")
        torneos.append([nombre, "Sin torneos en 2024", "", "", "", "", "", "", "", "", ""])
    else:
        for fila in filas:
            celdas = [td.text.strip() for td in fila.find_all('td')]
            if len(celdas) > 1:
                celdas.insert(0, nombre)  # Agregar el nombre del jugador como primera columna
                torneos.append(celdas)

        print(f"{nombre} añadido a la lista con {len(filas)} torneos.")

# Crear DataFrame para perfiles
df_perfil = pd.DataFrame({'Jugador': nombre_perf, 'Mejor posición OWGR': best_posicion, 'URL imagen': img_url})

# Crear DataFrame para torneos
columnas_torneos = ['Jugador', 'Evento', 'Tour', 'Semana', 'Año', 'Posición', 'Puntos ganados', 'Peso', 'Puntos ajustados', 'Posición OWGR anterior', 'Posición OWGR final']
df_torneos = pd.DataFrame(torneos, columns=columnas_torneos)

# Guardar CSVs
df_torneos.to_csv(csv_torneos, index=False)
df_perfil.to_csv(csv_jugador_foto, index=False)
