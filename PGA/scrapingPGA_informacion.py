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
csv_profiles = 'C:\\NAS_PAU\\TFG\\PGA\\PGAprofiles.csv'
csv_informacion_jugador = 'C:\\NAS_PAU\\TFG\\PGA\\PGAinformacionjugadores201-250.csv'
carpeta_img_perfil = 'C:\\NAS_PAU\\TFG\\PGA\\FotosPerfil'

# Opciones Chrome WebDriver
options = webdriver.ChromeOptions()
options.page_load_strategy = 'normal' 
options.add_argument("--headless")
driver = Chrome(options=options)
driver.maximize_window()
driver.implicitly_wait(5)

# Leer perfiles desde el CSV
df = pd.read_csv(csv_profiles, sep=';')

# Extraer la segunda columna (indexada en 0, la segunda es la columna en posición 1)
perfiles = df.iloc[:, 1].tolist()
print(perfiles)

# Listas para almacenar datos
instagram_list = []
img_url_perf = []
nombre_perf = []
edad_perf = []
turned_pro_perf = []
nacimiento_perf = []
universidad_perf = []
eventos_perf = []
victorias_perf = []
segundo_perf = []
top10_perf = []
top25_perf = []
corteshechos_perf = []
corteseliminado_perf = []
abandonos_perf = []
dinero_perf = []


for perfil in perfiles[200:]:
    # Verificar si la página existe antes de abrirla en Selenium
    driver.get(perfil + '/results')

    # Obtener HTML
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(random.randint(3, 7))

    # Extraer nombre del jugador
    nombres = [span.text.strip() for span in soup.find_all('span', class_='chakra-text css-190em5d')]
    nombre_completo = " ".join(nombres)
    print(nombre_completo)  
    nombre_perf.append(nombre_completo)

    # Extraer edad del jugador
    edad = soup.find_all('span', 'chakra-text css-126477q')
    edad_numero = edad[0].text.strip()
    print(edad_numero + ' años')
    edad_perf.append(edad_numero)

    # Extraer año de inicio en PGA
    turned_pro = soup.find_all('span', 'chakra-text css-126477q')
    pro = turned_pro[1].text.strip()
    print('Turnerd Pro: ' + pro)
    turned_pro_perf.append(pro)

    # Lugar de nacimiento jugador
    lugar = soup.find_all('span', 'chakra-text css-126477q')
    lugar_nacimiento = lugar[2].text.strip()
    print('Lugar nacimiento: ' + lugar_nacimiento)
    nacimiento_perf.append(lugar_nacimiento)

    # Universidad del jugador
    uni = soup.find_all('span', 'chakra-text css-126477q')
    universidad = uni[3].text.strip()
    print('Universidad: ' + universidad)
    universidad_perf.append(universidad)

    # Extraer imagen del jugador
    try:
        foto = soup.find('div', {'class': 'css-tw6u9'})
        foto_jugador = foto.find('img', {'alt': nombre_completo}).get('src')
    except AttributeError:
        img_url_perf.append("El jugador no tiene foto en la PGA")
        foto_jugador = None
        
    # Guardar imagen
    if foto_jugador:
        url_valida = 'https://www.pgatour.com' + foto_jugador
        img_url_perf.append(url_valida)
        img_response = req.get(url_valida, stream=True)            
        file_path = path.join(carpeta_img_perfil, f"{nombre_completo}.jpg")  
        with open(file_path, "wb") as file:
            for chunk in img_response.iter_content(1024):
                file.write(chunk)
        print(f"Imagen guardada en: {file_path}")

    # Link instagram
    try:
        instagram_link = soup.find("div", {"class": "css-1x6q1s7"})
        if instagram_link:
            try:
                instagram = instagram_link.find('a', {'href': re.compile('instagram')}).get('href')
                instagram_list.append(instagram)
                print(f"Instagram del Jugador: {instagram}")
            except AttributeError:
                instagram_list.append("El jugador no tiene Instagram")
                print("El jugador no tiene Instagram")
        else:
            instagram_list.append("El jugador no tiene Instagram")
            print("El jugador no tiene Instagram")
    except AttributeError:
        instagram_list.append("El jugador no tiene Instagram")
        print("El jugador no tiene Instagram")

    # Cargar página results para obtener el nuevo html
    #driver.get(perfil)
    
    # Obtener HTML
    #html = driver.page_source
    #soup = BeautifulSoup(html, 'html.parser')

    # Apartado results (2024)
    #try:
        #results = driver.find_element(By.XPATH, "//button[@aria-label='Results']")
        #ActionChains(driver).move_to_element(results).click(results).perform()
        #time.sleep(random.randint(3,5))
    #except:
        # eventos_perf.append('-')
        # victorias_perf.append('-')
        # segundo_perf.append('-')
        # top10_perf.append('-')
        # top25_perf.append('-')
        # corteshechos_perf.append('-')
        # corteseliminado_perf.append('-')
        # abandonos_perf.append('-')
        # dinero_perf.append('-')
        # continue     
    try:
        anyo_2024 = driver.find_element(By.XPATH, "//button[@aria-label='Year']")
        ActionChains(driver).move_to_element(anyo_2024).click(anyo_2024).perform()
        time.sleep(random.randint(2,4))
    except:
        eventos_perf.append('-')
        victorias_perf.append('-')
        segundo_perf.append('-')
        top10_perf.append('-')
        top25_perf.append('-')
        corteshechos_perf.append('-')
        corteseliminado_perf.append('-')
        abandonos_perf.append('-')
        dinero_perf.append('-')
        continue
    try:
        anyo_2024_selec = driver.find_element(By.XPATH, "//button[text()='2024']")
        ActionChains(driver).move_to_element(anyo_2024_selec).click(anyo_2024_selec).perform()
        time.sleep(random.randint(2,4)) 
    except:
        eventos_perf.append('-')
        victorias_perf.append('-')
        segundo_perf.append('-')
        top10_perf.append('-')
        top25_perf.append('-')
        corteshechos_perf.append('-')
        corteseliminado_perf.append('-')
        abandonos_perf.append('-')
        dinero_perf.append('-')
        continue

    # Volver a cargar HTML
    time.sleep(random.randint(7, 10))
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Eventos jugados 2024
    eventos = soup.find_all('p', 'chakra-text css-tplryy')
    print(eventos)
    eventos_2024 = eventos[0].text.strip()
    print('Eventos PGA 2024: ' + eventos_2024)
    eventos_perf.append(eventos_2024)

    # Victorias 2024
    victorias = soup.find_all('p', 'chakra-text css-tplryy')
    victorias_2024 = victorias[1].text.strip()
    print('Victorias PGA 2024: ' + victorias_2024)
    victorias_perf.append(victorias_2024)

    # 2a posición 2024
    segundo = soup.find_all('p', 'chakra-text css-tplryy')
    segundo_2024 = segundo[2].text.strip()
    print('2a posición PGA 2024: ' + segundo_2024 + ' veces')
    segundo_perf.append(segundo_2024)

    # Top 10 2024
    top10 = soup.find_all('p', 'chakra-text css-tplryy')
    top10_2024 = top10[3].text.strip()
    print('Top 10 PGA 2024: ' + top10_2024 + ' veces')
    top10_perf.append(top10_2024)

    # Top 25 2024
    top25 = soup.find_all('p', 'chakra-text css-tplryy')
    top25_2024 = top25[4].text.strip()
    print('Top 25 PGA 2024: ' + top25_2024 + ' veces')
    top25_perf.append(top25_2024)

    # Cortes pasados 2024
    corteshechos = soup.find_all('p', 'chakra-text css-tplryy')
    corteshechos_2024 = corteshechos[5].text.strip()
    print('Cortes pasados PGA 2024: ' + corteshechos_2024)
    corteshechos_perf.append(corteshechos_2024)

    # Cortes no pasados 2024
    corteseliminado = soup.find_all('p', 'chakra-text css-tplryy')
    corteseliminado_2024 = corteseliminado[6].text.strip()
    print('Cortes no pasados PGA 2024: ' + corteseliminado_2024)
    corteseliminado_perf.append(corteseliminado_2024)

    # Abandonos 2024
    abandonos = soup.find_all('p', 'chakra-text css-tplryy')
    abandonos_2024 = abandonos[7].text.strip()
    print('Abandonos PGA 2024: ' + abandonos_2024)
    abandonos_perf.append(abandonos_2024)

    # Dinero oficial 2024
    dinero = soup.find_all('p', 'chakra-text css-tplryy')
    dinero_2024 = dinero[-1].text.strip()
    print('Dinero oficial PGA 2024: ' + dinero_2024)
    dinero_perf.append(dinero_2024)

# Crear DataFrame
#columnas = ['Jugador', 'Edad', 'Año profesional', 'Lugar nacimiento', 'Universidad', 'Instagram', 'Foto', 'Eventos PGA 2024', 'Victorias PGA 2024', '2a posiciónn PGA 2024',
#            'Top 10 PGA 2024', 'Top 25 PGA 2024', 'Cortes pasados PGA 2024', 'Cortes no pasados PGA 2024', 'Abandonos PGA 2024', 'Dinero oficial PGA 2024']
df_jugador = pd.DataFrame({'Jugador': nombre_perf, 'Edad': edad_perf, 'Año profesional': turned_pro_perf, 'Lugar nacimiento': nacimiento_perf, 'Universidad': universidad_perf, 'Instagram': instagram_list, 
                            'Foto': img_url_perf, 'Eventos PGA 2024': eventos_perf, 'Victorias PGA 2024': victorias_perf, '2a posiciónn PGA 2024': segundo_perf, 'Top 10 PGA 2024': top10_2024, 
                            'Top 25 PGA 2024': top25_perf, 'Cortes pasados PGA 2024': corteshechos_perf, 'Cortes no pasados PGA 2024': corteseliminado_perf, 'Abandonos PGA 2024': abandonos_perf, 
                            'Dinero oficial PGA 2024': dinero_perf})
    
# Pasar a csv
df_jugador.to_csv(csv_informacion_jugador, index=False)
    

    
