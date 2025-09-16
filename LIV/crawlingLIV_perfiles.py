import re
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

# Ruta del archivo csv que se va a generar con la informacion de los perfiles
csv_profiles = 'C:\\NAS_PAU\\TFG\\LIV\\LIVprofiles.csv'

# URL de la página
url = 'https://www.livgolf.com/teams'

# Opciones Chrome webdriver
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.page_load_strategy = 'normal' 
driver = Chrome(options=options)
driver.maximize_window()
driver.implicitly_wait(5)

# Se solicita la url
driver.get(url)
time.sleep(2)


# Se obtiene el html
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')


# Lista con los jugadores
urls_list = [a['href'] for a in soup.find_all("a", class_="flex flex-col rounded-lg border border-grey-on-light-200 bg-white")]
urls_list = list(set(urls_list))
driver.quit()

df_perfil = pd.DataFrame({'Perfil': urls_list})

# csv con url
df_perfil.to_csv(csv_profiles, index=False)
