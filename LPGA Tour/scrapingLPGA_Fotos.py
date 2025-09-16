import os
import random
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains, Chrome
from selenium.webdriver.common.by import By

# Carpeta para guardar solo imágenes de jugadoras
output_dir = 'C:\\NAS_PAU\\TFG\\LPGA\\imagenes_jugadoras'
os.makedirs(output_dir, exist_ok=True)

# URL del directorio
url = 'https://www.lpga.com/athletes/directory'

# Configuración de Selenium
options = webdriver.ChromeOptions()
#options.add_argument('--headless')  # Activa si quieres sin ventana
options.page_load_strategy = 'normal'

driver = Chrome(options=options)
driver.implicitly_wait(5)
driver.get(url)
time.sleep(2)

# Aceptar cookies si aparecen
try:
    cookies = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
    ActionChains(driver).move_to_element(cookies).click(cookies).perform()
except:
    pass

# Cargar más jugadoras
x = 0
max_scrolls = 10
while x < max_scrolls:
    try:
        boton = driver.find_element(By.XPATH, "//p[text()='VIEW MORE ATHLETES']/ancestor::button")
        ActionChains(driver).move_to_element(boton).click(boton).perform()
        time.sleep(random.randint(2, 4))
        x += 1
    except:
        break

# Obtener HTML completo
html = driver.page_source
driver.quit()
soup = BeautifulSoup(html, 'html.parser')

# Buscar todas las etiquetas <img>
img_tags = soup.find_all('img')
print(f"Se encontraron {len(img_tags)} imágenes en total.")

# Filtrar y descargar solo las que contienen '/players' en la URL
contador = 0
for img in img_tags:
    img_url = img.get("data-src") or img.get("src")
    if not img_url:
        continue

    if not ("/-/media/images/lpga/" in img_url or "/-/media/images/epson-tour/" in img_url):
        continue


    # Asegurar URL completa
    if img_url.startswith("/"):
        img_url = "https://www.lpga.com" + img_url

    # Definir extensión del archivo
    ext = img_url.split(".")[-1].split("?")[0]
    if len(ext) > 5 or "/" in ext:
        ext = "jpg"

    # Guardar con nombre secuencial
    contador += 1
    filename = f"jugadora_{contador:03d}.{ext}"
    filepath = os.path.join(output_dir, filename)

    # Descargar
    try:
        response = requests.get(img_url, headers={"User-Agent": "Mozilla/5.0"})
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"Descargada: {filename}")
    except Exception as e:
        print(f"Error al descargar {img_url}: {e}")
