from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Configuración del navegador (modo headless opcional)
options = Options()
options.add_argument("--headless")  # elimina esta línea si quieres ver el navegador
driver = webdriver.Chrome(options=options)

# Abrir la página
url = "https://www.spotrac.com/liv/rankings/year/_/year/2024"
driver.get(url)

# Esperar a que se cargue el contenido
time.sleep(10)  # puedes reemplazar con WebDriverWait si quieres algo más robusto

# Buscar la tabla
rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

data = []
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) >= 6:
        jugador = cols[1].text.strip()
        total_ganado = cols[13].text.strip()
        torneos = cols[7].text.strip()
        data.append([jugador, total_ganado, torneos])

# Cerrar navegador
driver.quit()
# Crear DataFrame
df = pd.DataFrame(data, columns=[
    "Jugador", "Total ganado", "Torneos jugados"
])

# Convertir torneos a numérico
df["Torneos jugados"] = pd.to_numeric(df["Torneos jugados"], errors="coerce")  

# Guardar a CSV
df.to_csv("liv_2024_ganancias_torneos.csv", index=False, sep =';')

print(df.head())
