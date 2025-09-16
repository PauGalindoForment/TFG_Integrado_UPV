import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

# Ruta del archivo csv que se va a generar con la informacion de los perfiles
csv_profiles = 'C:\\NAS_PAU\\TFG\\PGA\\PGAprofiles.csv'

# URL de la página
url = 'https://www.pgatour.com/players'

# Opciones Chrome webdriver
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.page_load_strategy = 'normal' 

driver = Chrome(options=options)
driver.implicitly_wait(5)

# Se solicita la url
driver.get(url)
time.sleep(2)
x = 0
while True:
    x +=1
    driver.execute_script('scrollBy(0,750)')
    time.sleep(0.1)
    if x > 80:
        break

# Se obtiene el html
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')


# Lista con los jugadores
urls_list = ['https://www.pgatour.com' + a['href'] for a in soup.select('.chakra-text.css-k9txqx a')]
print(urls_list)
print(len(urls_list))
driver.quit()

# Nombres
nombre = [a['aria-label'] for a in soup.select('.chakra-text.css-k9txqx a')]

# Dataframe
df_perfil = pd.DataFrame({'Jugador': nombre, 'URL perfil': urls_list})

# csv con url
df_perfil.to_csv(csv_profiles, index=False)