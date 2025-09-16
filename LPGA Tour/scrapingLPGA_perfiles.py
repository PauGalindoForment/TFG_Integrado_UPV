import random
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains, Chrome
from selenium.webdriver.common.by import By

# Ruta del archivo CSV que se va a generar con la información de los perfiles
csv_profiles = 'C:\\NAS_PAU\\TFG\\LPGA\\LPGAprofiles.csv'

# URL de la página
url = 'https://www.lpga.com/athletes/directory'

# Opciones Chrome webdriver
options = webdriver.ChromeOptions()
#options.add_argument('--headless')  # Descomentar si quieres usar sin interfaz gráfica
options.page_load_strategy = 'normal'

driver = Chrome(options=options)
driver.implicitly_wait(5)

# Se solicita la URL
driver.get(url)
time.sleep(2)

# Cookies
cookies = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
ActionChains(driver).move_to_element(cookies).click(cookies).perform()

# Intentar hacer click en 'VIEW MORE ATHLETES' para cargar más jugadores
x = 0
max_scrolls = 10  # Puedes aumentar este número si necesitas cargar más jugadores
while x < max_scrolls:
    try:
        mas_jugadoras = driver.find_element(By.XPATH, "//p[text()='VIEW MORE ATHLETES']/ancestor::button")
        ActionChains(driver).move_to_element(mas_jugadoras).click(mas_jugadoras).perform()
        time.sleep(random.randint(2, 4))  # Tiempo de espera aleatorio
        x += 1
    except:
        print("Se ha llegado al final o hubo un error al intentar hacer clic.")
        break

# Se obtiene el HTML
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Listar las URLs de los perfiles
urls_list = ['https://www.lpga.com' + a['href'] for a in soup.select("a[href^='/athletes/']")]

# Obtener los nombres de las jugadoras
names = [a.find("span", class_="is_SizableText").text.strip() for a in soup.select("a[href^='/athletes/']")]

# Verificar si las listas están correctas
print(names)
print(urls_list)

# Crear un DataFrame con los nombres y las URLs
df_perfil = pd.DataFrame({
    'Jugadora': names,
    'URL perfil': urls_list
})

# Guardar el DataFrame en un archivo CSV
df_perfil.to_csv(csv_profiles, index=False)

print(f"CSV guardado con {len(df_perfil)} perfiles en {csv_profiles}")

# Cerrar el navegador
driver.quit()
