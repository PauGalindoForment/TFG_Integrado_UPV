import re
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import csv

# Ruta del archivo csv que se va a generar con los perfiles
csv_profiles = 'C:\\NAS_PAU\\TFG\\OWGR\\OWGRprofiles03022025.csv'
csv_torneos = 'C:\\NAS_PAU\\TFG\\OWGR\\OWGRtorneosjugador.csv'

#URL de la página
url = 'https://www.owgr.com/current-world-ranking'

#Opciones Chrome webdriver
options = webdriver.ChromeOptions()
options.page_load_strategy = 'normal' 

options.add_argument("--headless")
driver = Chrome(options=options)
driver.implicitly_wait(1)

#Se solicita la url
driver.get(url)
time.sleep(1)

# Cookies
cookies = driver.find_element(By.CLASS_NAME, 'regularButton_button__n3ye_')
ActionChains(driver).move_to_element(cookies).click(cookies).perform()

#Lista con los jugadores (4700), se vuelve a pasar el html/soup para que coja el html por cada una de las páginas
b = 47
urls_list = []
while b > 0:
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    urls_list += ['https://www.owgr.com' + a['href'] for a in soup.select('.textLink_container__WoRMe.undefined')]
    elemento = driver.find_element(By.CLASS_NAME, 'next')
    ActionChains(driver).move_to_element(elemento).click(elemento).perform()
    b = b - 1
    time.sleep(1)
print(urls_list)
print(len(urls_list))
with open(csv_profiles, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows([[url] for url in urls_list])
driver.quit()

# Lista donde se almacenarán los datos
datos = []

# Se abre la url de cada perfil de jugador
for url_profile in urls_list[:5]:
    url_2024 = url_profile + '?tab=events&year=2024'
    options.add_argument("--headless")
    driver = Chrome(options=options)
    driver.implicitly_wait(1)
    driver.get(url_2024)
    time.sleep(1)

#Se obtiene el html
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

# Cookies
    cookies = driver.find_element(By.CLASS_NAME, 'regularButton_button__n3ye_')
    ActionChains(driver).move_to_element(cookies).click(cookies).perform()

# Extraer cada torneo junto con el jugador
    filas = soup.find_all('tr')
    for fila in filas:
        celdas = [td.text.strip() for td in fila.find_all('td')]  
        nom = soup.find('div', {'class':'playerInfoView_player__name__mjkdj'})
        mejor_p = soup.find('div', {'class':'playerStatisticsView_element__value__sHVly'})
        nombre = nom.text.strip()
        mejor_posicion = mejor_p.text.strip()
        celdas.insert(0, nombre)
        celdas.append(mejor_posicion)
        if len(celdas) > 1: 
            datos.append(celdas)

# Crear DataFrame
columas = ['Jugador', 'Evento', 'Tour', 'Semana', 'Año', 'Posición', 'Puntos ganados', 'Peso', 'Puntos ajustados', 'Posición OWGR anterior', 'Posición OWGR final', 'Mejor posición OWGR']
df = pd.DataFrame(datos, columns=columas)

# Guardar csv con todos los torneos por jugador
df.to_csv(csv_torneos, index=False)

