from concurrent.futures import wait
import os
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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Ruta del archivo csv que se va a generar con la informacion de los perfiles
csv_profiles = 'C:\\NAS_PAU\\TFG\\LPGA\\LPGAprofiles.csv'
csv_informacion_jugador = 'C:\\NAS_PAU\\TFG\\LPGA\\LPGAinformacionjugadoras1-100.csv'
carpeta_img_perfil = 'C:\\NAS_PAU\\TFG\\LPGA\\FotosPerfil'

# Opciones Chrome WebDriver
options = webdriver.ChromeOptions()
options.page_load_strategy = 'normal' 
#options.add_argument("--headless")
driver = Chrome(options=options)
driver.maximize_window()
driver.implicitly_wait(5)

# Leer perfiles desde el CSV
df = pd.read_csv(csv_profiles, sep=',')

# Extraer la segunda columna (indexada en 0, la segunda es la columna en posición 1)
perfiles = df.iloc[:, 1].tolist()

# Listas para almacenar datos
img_url_perf = []
nombre_perf = []
pais_perf = []
edad_perf = []
rookie_year_perf = []
eventos_perf = []
victorias_perf = []
top10_perf = []
corteshechos_perf = []
dinero_perf = []


for perfil in perfiles[2:10]:
    # Verificar si la página existe antes de abrirla en Selenium
    driver.get(perfil)
    time.sleep(random.randint(5, 17))

    # Obtener HTML
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Extraer nombre del jugador
    nombres = [span.text.strip() for span in soup.find_all('span', class_='is_SizableText font_heading _col-_md_2142325188 _ff-_md_299667014 _fow-_md_1366435823 _ls-_md_905096962 _fos-_md_1477258343 _lh-_md_1677662400 _bxs-border-box _ww-break-word _whiteSpace-pre-wrap _mt-0px _mr-0px _mb-0px _ml-0px _col-2142325188 _ff-299667014 _fow-233016078 _ls-167743997 _fos-2rem _lh-222976511 _dsp-block _ta-left')]
    nombre_completo = " ".join(nombres)
    print(nombre_completo)  
    nombre_perf.append(nombre_completo)

    #Extraer país de la jugadora
    pais = soup.find('p', class_='is_SizableText font_body _col-_md_2142325188 _ff-_md_299667014 _fow-_md_1366434738 _ls-_md_905098047 _fos-_md_1477257258 _lh-_md_1677661315 _bxs-border-box _ww-break-word _whiteSpace-nowrap _mt-0px _mr-0px _mb-0px _ml-0px _col-2142325188 _ff-299667014 _fow-1366436691 _ls-905096094 _fos-1477259211 _lh-1677663268 _dsp-block _tt-uppercase _maw-10037 _ox-hidden _oy-hidden _textOverflow-ellipsis').text.strip()
    print(pais)
    pais_perf.append(pais)

    # Extraer edad del jugador
    edad = soup.find('h2', string=re.compile(r'\bis\b \d{2}\b.*years old'))
    match = re.search(r'\bis (\d{2}) years old', edad.text)
    edad_numero = int(match.group(1))
    print(str(edad_numero) + ' años')
    edad_perf.append(edad_numero)

    # Extraer año de inicio en LPGA
    rookie_year = soup.find('h2', string=re.compile(r'joined the LPGA Tour in \d{4}'))
    match = re.search(r'joined the LPGA Tour in (\d{4})', rookie_year.text)
    rookie = int(match.group(1))
    print('Rookie year: ' + str(rookie))
    rookie_year_perf.append(rookie)

    # Extraer imagen del jugador
    try:
        # Buscar imagen del jugador en la página
        img_tag = soup.find('img', src=re.compile(r"/-/media/images/lpga/players/"))
        if img_tag:
            foto_jugadora = "https://www.lpga.com" + img_tag['src']
        else:
            foto_jugadora = None
    except Exception as e:
        print(f"Error buscando imagen: {e}")
        foto_jugadora = None

    # Descargar y guardar imagen
    if foto_jugadora:
        img_url_perf.append(foto_jugadora)
        try:
            img_response = req.get(foto_jugadora, stream=True)
            img_response.raise_for_status()
            file_path = os.path.join(carpeta_img_perfil, f"{nombre_completo}.jpg")
            with open(file_path, "wb") as file:
                for chunk in img_response.iter_content(1024):
                    file.write(chunk)
            print(f"Imagen guardada en: {file_path}")
        except Exception as e:
            print(f"Error al descargar imagen: {e}")
    else:
        img_url_perf.append("No disponible")
        print(f"No se encontró imagen para {nombre_completo}")

    #Cargar página results para obtener el nuevo html
    url_results = perfil.replace('/overview', '/results')
    driver.get(url_results)
    driver.implicitly_wait(3)
    time.sleep(random.randint(5,7))

    # Cookies
    try:
        cookies = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        ActionChains(driver).move_to_element(cookies).click(cookies).perform()
    except:
        print('Cookies aceptadas')

    try:
        print("🔄 Esperando que la página cargue el botón 'Seasons' visible en el DOM...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'Seasons')]"))
        )
        print("Botón 'Seasons' detectado en el DOM.")

        # Ahora esperar que sea clickeable
        seasons_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Seasons')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", seasons_button)
        driver.execute_script("arguments[0].click();", seasons_button)
        print("Clic realizado en 'Seasons'.")

        # Seleccionar 2024
        print("Esperando opción '2024'...")
        option_2024 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[.='2024']"))
        )
        driver.execute_script("arguments[0].click();", option_2024)
        print("Año 2024 seleccionado.")
        time.sleep(2)

    except Exception as e:
        print(f"Fallo en selección de año 2024: {e}")
        eventos_perf.append('-')
        victorias_perf.append('-')
        top10_perf.append('-')
        corteshechos_perf.append('-')
        dinero_perf.append('-')
        continue
    # Volver a cargar HTML
    time.sleep(random.randint(5, 7))
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Eventos jugados 2024
    eventos = soup.find_all('span', 'is_SizableText font_heading _col-_md_748454664 _ff-_md_299667014 _fow-_md_1366435792 _ls-_md_905096993 _fos-_md_1477258312 _lh-_md_1677662369 _bxs-border-box _ww-break-word _whiteSpace-pre-wrap _mt-0px _mr-0px _mb-0px _ml-0px _col-748454664 _ff-299667014 _fow-233016109 _ls-167744028 _fos-229441189 _lh-222976542 _dsp-block _ta-left')
    eventos_2024 = eventos[0].text.strip()
    print('Eventos LPGA 2024: ' + eventos_2024)
    eventos_perf.append(eventos_2024)

    # Victorias 2024
    victorias = soup.find_all('span', 'is_SizableText font_heading _col-_md_748454664 _ff-_md_299667014 _fow-_md_1366435792 _ls-_md_905096993 _fos-_md_1477258312 _lh-_md_1677662369 _bxs-border-box _ww-break-word _whiteSpace-pre-wrap _mt-0px _mr-0px _mb-0px _ml-0px _col-748454664 _ff-299667014 _fow-233016109 _ls-167744028 _fos-229441189 _lh-222976542 _dsp-block _ta-left')
    victorias_2024 = victorias[3].text.strip()
    print('Victorias PGA 2024: ' + victorias_2024)
    victorias_perf.append(victorias_2024)

    # Top 10 2024
    top10 = soup.find_all('span', 'is_SizableText font_heading _col-_md_748454664 _ff-_md_299667014 _fow-_md_1366435792 _ls-_md_905096993 _fos-_md_1477258312 _lh-_md_1677662369 _bxs-border-box _ww-break-word _whiteSpace-pre-wrap _mt-0px _mr-0px _mb-0px _ml-0px _col-748454664 _ff-299667014 _fow-233016109 _ls-167744028 _fos-229441189 _lh-222976542 _dsp-block _ta-left')
    top10_2024 = top10[2].text.strip()
    print('Top 10 PGA 2024: ' + top10_2024 + ' veces')
    top10_perf.append(top10_2024)

    # Cortes pasados 2024
    corteshechos = soup.find_all('span', 'is_SizableText font_heading _col-_md_748454664 _ff-_md_299667014 _fow-_md_1366435792 _ls-_md_905096993 _fos-_md_1477258312 _lh-_md_1677662369 _bxs-border-box _ww-break-word _whiteSpace-pre-wrap _mt-0px _mr-0px _mb-0px _ml-0px _col-748454664 _ff-299667014 _fow-233016109 _ls-167744028 _fos-229441189 _lh-222976542 _dsp-block _ta-left')
    corteshechos_2024 = corteshechos[1].text.strip()
    print('Cortes pasados PGA 2024: ' + corteshechos_2024)
    corteshechos_perf.append(corteshechos_2024)

    # Dinero oficial 2024
    dinero = soup.find_all('span', 'is_SizableText font_heading _col-_md_748454664 _ff-_md_299667014 _fow-_md_1366435792 _ls-_md_905096993 _fos-_md_1477258312 _lh-_md_1677662369 _bxs-border-box _ww-break-word _whiteSpace-pre-wrap _mt-0px _mr-0px _mb-0px _ml-0px _col-748454664 _ff-299667014 _fow-233016109 _ls-167744028 _fos-229441189 _lh-222976542 _dsp-block _ta-left')
    dinero_2024 = dinero[-1].text.strip()
    print('Dinero oficial PGA 2024: ' + dinero_2024)
    dinero_perf.append(dinero_2024)

    df_jugador = pd.DataFrame({'Jugadora': nombre_perf, 'Edad': edad_perf, 'Año inicio LPGA': rookie_year_perf, 'País': pais_perf, 'Foto': img_url_perf, 'Eventos LPGA 2024': eventos_perf, 
                                'Victorias LPGA 2024': victorias_perf, 'Top 10 PGA 2024': top10_perf,'Cortes pasados PGA 2024': corteshechos_perf, 
                                'Dinero oficial PGA 2024': dinero_perf})
        
    # Pasar a csv
    df_jugador.to_csv(csv_informacion_jugador, index=False)
    

    

