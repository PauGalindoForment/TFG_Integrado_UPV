from os import path
import re
import requests as req
import time
import pandas as pd
import csv
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


# Ruta del archivo csv que se va a generar con la informacion de los perfiles
csv_profiles = 'C:\\NAS_PAU\\TFG\\LIV\\LIVprofiles.csv'
csv_informacion_jugador = 'C:\\NAS_PAU\\TFG\\LIV\\LIVinformacionjugadores.csv'
carpeta_img_perfil = 'C:\\NAS_PAU\\TFG\\LIV\\FotosPerfil'

# Opciones Chrome WebDriver
options = webdriver.ChromeOptions()
options.page_load_strategy = 'normal' 
options.add_argument("--headless")
driver = Chrome(options=options)
driver.maximize_window()
driver.implicitly_wait(5)

# Leer perfiles desde el CSV
df = pd.read_csv(csv_profiles, sep=';')
perfiles = df.iloc[:,0].tolist()

# Listas para almacenar datos
instagram_list = []
img_url_perf = []
nombre_perf = []
edad_perf = []
turned_pro_perf = []
liv_debut_perf = []
pais_perf = []
equipo_perf = []

for perfil in perfiles:
    # Verificar si la página existe antes de abrirla en Selenium
    driver.get(perfil)
    driver.maximize_window()

    # Obtener HTML
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(random.randint(3, 7))


    # Extraer nombre del jugador
    nombres = soup.find_all('span', class_='font-heading headings-font-weight headings-text-transform text-[1.25rem] leading-[1.1] lg:text-[1.5rem]')
    apellidos = soup.find_all('span', class_='font-heading headings-font-weight headings-text-transform text-[1.5rem] leading-[1.1] lg:text-[2.125rem]')
    nombre_completo = nombres[0].text.strip()+ ' ' + apellidos[0].text.strip()
    print(nombre_completo)  
    # nombre_perf.append(nombre_completo)

    # Extraer edad del jugador
    try:
        edad = soup.find_all('p', 'font-subtitle font-bold text-[0.75rem] leading-[1.4] lg:text-[0.875rem]')
        edad_numero = edad[0].text.strip()
        print(edad_numero + ' años')
        edad_perf.append(edad_numero)
    except:
        edad_perf.append('-')

    # Extraer año de inicio profesional
    try:
        turned_pro = soup.find_all('p', 'font-subtitle font-bold text-[0.75rem] leading-[1.4] lg:text-[0.875rem]')
        pro = turned_pro[1].text.strip()
        print('Turnerd Pro: ' + pro)
        turned_pro_perf.append(pro)
    except:
        turned_pro_perf.append('-')

    # Extraer año de inicio LIV
    try:
        liv = soup.find_all('p', 'font-subtitle font-bold text-[0.75rem] leading-[1.4] lg:text-[0.875rem]')
        liv_debut = liv[2].text.strip()
        print('LIV debut: ' + liv_debut)
        liv_debut_perf.append(liv_debut)
    except:
        liv_debut_perf.append('-')

    # País
    pais = soup.find_all('abbr', 'font-subtitle font-bold text-[0.875rem] leading-[1.4] lg:text-[1rem] border-none no-underline')
    pais_jug = pais[0].text.strip()
    print('País: ' + pais_jug)
    pais_perf.append(pais_jug)

    # Equipo
    equipo = soup.find_all('p', 'font-subtitle font-bold text-[0.875rem] leading-[1.4] lg:text-[1rem]')
    equipo_liv = equipo[0].text.strip()
    print('Equipo: ' + equipo_liv)
    equipo_perf.append(equipo_liv)

    # Instagram
    try:
        instagram = soup.find('a', 'hover:opacity-75')['href']
        print('Instagram: ' + instagram)
        instagram_list.append(instagram)
    except:
        instagram_list.append("El jugador no tiene Instagram")
        print("El jugador no tiene Instagram")
        
    #Extraer imagen del jugador
    try:
        foto_jugador = soup.find('img', {'alt': nombre_completo}).get('src')
    except AttributeError:
        img_url_perf.append("El jugador no tiene foto en el LIV")
        foto_jugador = None
        
    # Guardar imagen
    if foto_jugador:
        img_response = req.get(foto_jugador, stream=True)            
        file_path = path.join(carpeta_img_perfil, f"{nombre_completo}.jpg")  
        with open(file_path, "wb") as file:
            for chunk in img_response.iter_content(1024):
                file.write(chunk)
        print(f"Imagen guardada en: {file_path}")

# DataFrame
df_informacion = pd.DataFrame({'Nombre': nombre_perf, 'Edad': edad_perf, 'Inicio Profesional': turned_pro_perf, 'Inicio LIV': liv_debut_perf, 'País': pais_perf, 'Equipo':equipo_perf, 'Instagram': instagram_list})

# To csv
df_informacion.to_csv(csv_informacion_jugador, index=False)
