import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains, Chrome
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Configuración del navegador
options = webdriver.ChromeOptions()
options.page_load_strategy = 'normal'
driver = Chrome(options=options)
driver.implicitly_wait(5)

# Cargar la página
url = 'https://www.lpga.com/athletes/directory'
driver.get(url)
time.sleep(2)

# Aceptar cookies
try:
    cookies = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
    ActionChains(driver).move_to_element(cookies).click(cookies).perform()
except:
    pass

# Cargar todas las jugadoras
for _ in range(10):
    try:
        boton = driver.find_element(By.XPATH, "//p[text()='VIEW MORE ATHLETES']/ancestor::button")
        ActionChains(driver).move_to_element(boton).click(boton).perform()
        time.sleep(random.uniform(2, 4))
    except:
        break

# Extraer HTML
html = driver.page_source
driver.quit()

# Parsear con BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
name_tags = soup.find_all("span", class_="is_SizableText")
names = [tag.text.strip() for tag in name_tags if tag.text.strip()]

# Guardar en Excel
df = pd.DataFrame(names, columns=["Jugadora"])
df.to_excel("nombres_jugadoras.xlsx", index=False)
print(f"{len(df)} nombres guardados en 'nombres_jugadoras.xlsx'")

