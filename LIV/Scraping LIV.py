import re
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By




#URL de la página
url = 'https://www.livgolf.com/player'

#Opciones Chrome webdriver
options = webdriver.ChromeOptions()

driver = Chrome(options=options)
driver.implicitly_wait(2)

#Se solicita la url
driver.get(url)
driver.maximize_window()
time.sleep(2)

#Se obtiene el html
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

#Lista con los jugadores
urls_list = ['https://www.livgolf.com' + a['href'] for a in soup.select('.last\\:border-b-thin.border-l-thin.border-t-thin.relative.grid.grid-cols-2.flex-col-reverse.items-end.sm\\:grid-cols-\\[12rem\\,auto\\].md\\:flex.md\\:flex-col.md\\:border-none.md\\:p-0')]
print(urls_list)
print(len(urls_list))
driver.quit()


#LISTA PARA ALMACENAR LOS DIFERENTES LINKS DE INSTAGRAM

instagram_list = []

for url in urls_list:
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(2)
    pl_html = driver.page_source
    pl_soup = BeautifulSoup(pl_html, 'html.parser')
#OBTENCION DE LINK DE INSTAGRAM
    try:
        instagram_link = pl_soup.find("div", {"class": "flex gap-5 lg:gap-8"})
        if instagram_link:
            try:
                instagram = instagram_link.find('a', {'href': re.compile(r'instagram', re.I)}).get('href')
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
driver.quit()
