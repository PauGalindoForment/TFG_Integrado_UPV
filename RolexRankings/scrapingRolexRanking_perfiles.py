import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import csv

# Ruta del archivo csv que se va a generar con los perfiles
csv_profiles = 'C:\\NAS_PAU\\TFG\\RolexRanking\\RolexRankingprofiles2.csv'

#URL de la página
url = 'https://www.rolexrankings.com/es/rankings'

#Opciones Chrome webdriver
options = webdriver.ChromeOptions()
options.page_load_strategy = 'normal' 

driver = Chrome(options=options)
driver.implicitly_wait(1)

#Se solicita la url
driver.get(url)
time.sleep(10)

#Lista con las jugadoras (1592), 50 por click
b = 31
urls_list = []
while b > 0:
    elemento = driver.find_element(By.CLASS_NAME, '_3Qqxt')
    ActionChains(driver).move_to_element(elemento).click(elemento).perform()
    b = b - 1
    time.sleep(1)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
lista =  soup.find_all( 'td', {'class':'_2Dx28'})
nombre = [td.find('a').text.strip() for td in lista if td.find('a')]
urls_list = ['https://www.rolexrankings.com' + td.find('a')['href'] for td in lista if td.find('a')]
driver.quit()
print(urls_list)
print(len(urls_list))
df_perfil = pd.DataFrame({'Jugadora': nombre, 'URL perfil': urls_list})
df_perfil.to_csv(csv_profiles, index=False, sep=';')

