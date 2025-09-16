from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# Configuración
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)
driver.maximize_window()

# URL del perfil del jugador
url = "https://www.livgolf.com/player/jon-rahm"
driver.get(url)
time.sleep(5)  # aseguramos que cargue el contenido

# Hacer scroll para garantizar visibilidad
driver.execute_script("window.scrollTo(0, 300);")
time.sleep(1)

# Abrir desplegable del año
try:
    boton_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'2024')]")))
    ActionChains(driver).move_to_element(boton_dropdown).click().perform()
    time.sleep(1)
except Exception as e:
    print("⚠️ No se pudo abrir el menú de años:", e)

# Seleccionar el año 2024 del menú
try:
    opcion_2024 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='2024']")))
    driver.execute_script("arguments[0].click();", opcion_2024)  # click forzado vía JS
    time.sleep(2)
except Exception as e:
    print("⚠️ No se pudo hacer clic en '2024':", e)

# Scraping de la tabla (como ya tenías)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

try:
    nombre = soup.find('h1').get_text(strip=True)
except:
    nombre = "NombreDesconocido"

try:
    tabla = soup.find('table', class_='w-full border-collapse')
    rows = tabla.find('tbody').find_all('tr')
except:
    rows = []

datos = []
for row in rows:
    cols = row.find_all('td')
    fila = [col.get_text(strip=True) for col in cols]
    fila.insert(0, nombre)
    datos.append(fila)

driver.quit()

# Crear DataFrame y guardar
df = pd.DataFrame(datos, columns=['Nombre', 'Evento', 'Fecha', 'Posición', 'Puntos', 'Score'])
df.to_csv("resultados_rahm_2024.csv", index=False, sep=';')
print("✅ Datos guardados en resultados_rahm_2024.csv")
