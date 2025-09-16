import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Ruta CSV
csv_ganancias2024_LPGA = 'C:\\NAS_PAU\\TFG\\LPGA\\LPGAeventos2024.csv'

# Configurar Selenium
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get('https://www.lpga.com/stats-and-rankings/money-and-finishes')
time.sleep(25)  # Aumenta si hace falta

# Extraer HTML completo
html = driver.page_source
driver.quit()

# Parsear con BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Buscar tabla con role="table"
table = soup.find(attrs={"role": "table"})
if not table:
    raise Exception("No se encontró la tabla con role='table'.")

# Extraer encabezados
headers = [h.text.strip() for h in table.find_all(attrs={"role": "columnheader"})]

# Extraer filas
rows = []
for row in table.find_all(attrs={"role": "row"}):
    cells = row.find_all(attrs={"role": ["cell", "gridcell"]})
    values = [c.text.strip() for c in cells]
    if values:
        rows.append(values)

# Crear DataFrame y guardar
if rows:
    df = pd.DataFrame(rows, columns=headers[:len(rows[0])])
    df.to_csv(csv_ganancias2024_LPGA, index=False, sep=";", encoding="utf-8")
    print("CSV generado con", len(df), "jugadoras.")
else:
    print("No se extrajeron datos de filas.")
