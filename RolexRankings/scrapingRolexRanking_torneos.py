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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Ruta del archivo csv
csv_profiles = 'C:\\NAS_PAU\\TFG\\RolexRanking\\Jugadoras_con_perfil_filtrado.xlsx'
csv_torneos = 'C:\\NAS_PAU\\TFG\\RolexRanking\\RolexRankingtorneosjugadoraTotal2.csv'

# Opciones Chrome WebDriver
options = webdriver.ChromeOptions()
options.page_load_strategy = 'normal' 
options.add_argument("--headless")
driver = Chrome(options=options)
driver.implicitly_wait(5)

# Listas para almacenar datos
torneos = []

# Controlar las jugadoras que se procesarán por ejecución
perfiles = []
num_prev = 0
num_post = 1000

# Leer perfiles desde el CSV
df = pd.read_excel(csv_profiles)

# Extraer la segunda columna 
perfiles = df.iloc[:, 1].tolist()
print(perfiles)

# Procesar cada jugadora
for perfil in perfiles[num_prev:]:
    response = req.get(perfil)

    if response.status_code != 200:
        print(f"Página no encontrada para {perfil}. La jugadora ya no existe en Rolex Ranking.")
        nombre = perfil.split('/')[-1]  
        torneos.append([nombre, "Perfil no encontrado", "", "", "", "", "", ""])
        continue  
    driver.get(perfil)
    time.sleep(1)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
    except TimeoutException:
        print(f"Tiempo de espera agotado para {perfil}. No se encontraron torneos.")

    # Intentar hacer clic hasta 3 veces en el botón "Ver más" si existe
    for intento in range(3):
        try:
            boton = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, '_26UAJ'))
            )
            ActionChains(driver).move_to_element(boton).click(boton).perform()
            time.sleep(2) 
        except TimeoutException:
            break


    # Obtener HTML
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    for noscript in soup.find_all('noscript'):
        noscript.decompose()

    def es_numero(valor):
        try:
            int(valor) 
            return True
        except ValueError:
            return False 
    
    # Extraer información de la jugadora
    nombre = soup.find('h2').text.strip()
    
    # Extraer torneos
    filas = soup.find_all('tr')
    num_torneos = 0

    if not filas:
        print(f"No se encontraron torneos para {nombre} en 2024.")
        torneos.append([nombre, "Sin torneos en 2024", "", "", "", "", "", ""])
    else:
        for fila in filas:
            celdas = [td.text.strip() for td in fila.find_all('td')]
            if len(celdas) > 1:
                if celdas[3] == '2024' and not es_numero(celdas[0]):
                    celdas.insert(0, nombre) 
                    torneos.append(celdas)
                    num_torneos = num_torneos + 1

        print(f"{nombre} añadido a la lista con {num_torneos } torneos.")

# Crear DataFrame para torneos
columnas_torneos = ['Jugadora', 'Evento', 'Tour', 'Semana', 'Año', 'Posición', 'Puntos ganados', 'Posición Rolex Ranking final']
df_torneos = pd.DataFrame(torneos, columns=columnas_torneos)

# Eliminar duplicados
df_torneos.drop_duplicates(inplace=True)

# Guardar CSVs
df_torneos.to_csv(csv_torneos, index=False, sep=';')


