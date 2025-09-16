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
csv_ganancias2024_LIV = 'C:\\NAS_PAU\\TFG\\LIV\\LIVganancias2024.csv'

# Opciones Chrome WebDriver
options = webdriver.ChromeOptions()
options.page_load_strategy = 'normal' 
options.add_argument("--headless")
driver = Chrome(options=options)
driver.maximize_window()
driver.implicitly_wait(5)

# Se solicita la url
driver.get('https://www.golfmonthly.com/news/liv-golf-money-list-how-much-every-player-has-earned-in-2024')
time.sleep(2)

# Se obtiene el html
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Busca la tabla en la página
table = soup.find("table")  
    
# Extraer los encabezados
headers = [header.text.strip() for header in table.find_all("th")]

# Extraer las filas de la tabla
rows = []
for row in table.find_all("tr")[1:]:  # Saltamos la primera fila (encabezados)
    cols = [col.text.strip() for col in row.find_all("td")]
    rows.append(cols)

# Crear un DataFrame con pandas
df = pd.DataFrame(rows, columns=headers)

# Guardar en CSV
df.to_csv(csv_ganancias2024_LIV, index=False)