import os
import re
import time
import random
import requests as req
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome

# Rutas
csv_profiles = 'C:\\NAS_PAU\\TFG\\LPGA\\LPGAprofiles.csv'
csv_informacion_jugador = 'C:\\NAS_PAU\\TFG\\LPGA\\LPGAinformacion_overview.csv'
carpeta_img_perfil = 'C:\\NAS_PAU\\TFG\\LPGA\\FotosPerfil'

# Configuración navegador
options = webdriver.ChromeOptions()
options.page_load_strategy = 'normal'
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
driver = Chrome(options=options)
driver.maximize_window()
driver.implicitly_wait(5)

# Leer CSV de perfiles
df = pd.read_csv(csv_profiles, sep=',')
perfiles = df.iloc[:, 1].tolist()

# Listas de datos
img_url_perf = []
nombre_perf = []
pais_perf = []
edad_perf = []
rookie_year_perf = []

# Bucle principal
for perfil in perfiles:
    driver.get(perfil)
    time.sleep(random.randint(15, 20))

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Nombre (dos clases posibles)
    try:
        clases_nombre = [
            "is_SizableText font_heading _col-_md_2142325188 _ff-_md_299667014 _fow-_md_1366435823 _ls-_md_905096962 _fos-_md_1477258343 _lh-_md_1677662400 _bxs-border-box _ww-break-word _whiteSpace-pre-wrap _mt-0px _mr-0px _mb-0px _ml-0px _col-2142325188 _ff-299667014 _fow-233016078 _ls-167743997 _fos-229441158 _lh-222976511 _dsp-block _ta-left",
            "is_SizableText font_heading _col-_md_2142325188 _ff-_md_299667014 _fow-_md_1366435823 _ls-_md_905096962 _fos-_md_1477258343 _lh-_md_1677662400 _bxs-border-box _ww-break-word _whiteSpace-pre-wrap _mt-0px _mr-0px _mb-0px _ml-0px _col-2142325188 _ff-299667014 _fow-233016078 _ls-167743997 _fos-2rem _lh-222976511 _dsp-block _ta-left"
        ]

        nombres = []
        for clase in clases_nombre:
            spans = soup.find_all("span", class_=clase)
            for span in spans:
                texto = span.text.strip()
                if texto:
                    nombres.append(texto)

        nombre_completo = " ".join(nombres) if nombres else "-"
    except:
        nombre_completo = "-"
    print(nombre_completo)
    nombre_perf.append(nombre_completo)

    # País (dos clases posibles)
    try:
        clases_pais = [
            "is_SizableText font_body _col-_md_2142325188 _ff-_md_299667014 _fow-_md_1366434738 _ls-_md_905098047 _fos-_md_1477257258 _lh-_md_1677661315 _bxs-border-box _ww-break-word _whiteSpace-nowrap _mt-0px _mr-0px _mb-0px _ml-0px _col-2142325188 _ff-299667014 _fow-1366436691 _ls-905096094 _fos-1477259211 _lh-1677663268 _dsp-block _tt-uppercase _maw-10037 _ox-hidden _oy-hidden _textOverflow-ellipsis",
            "is_SizableText font_body _col-_md_2142325188 _ff-_md_299667014 _fow-_md_1366435668 _ls-_md_905097117 _fos-_md_1477258188 _lh-_md_1677662245 _bxs-border-box _ww-break-word _mt-0px _mr-0px _mb-0px _ml-0px _col-2142325188 _ff-299667014 _fow-233016233 _ls-167744152 _fos-229441313 _lh-222976666 _ta-left"
        ]
        pais = "-"
        for clase in clases_pais:
            tag = soup.find(lambda t: t.name in ["p", "span"] and t.get("class") and " ".join(t["class"]) == clase)
            if tag and tag.text.strip():
                pais = tag.text.strip()
                break
    except:
        pais = "-"

    print(pais)
    pais_perf.append(pais)

    # Edad
    try:
        edad = soup.find('h2', string=re.compile(r'\bis\b \d{2}\b.*years old'))
        match = re.search(r'\bis (\d{2}) years old', edad.text)
        edad_numero = int(match.group(1))
    except:
        edad_numero = "-"
    print(str(edad_numero) + ' años')
    edad_perf.append(edad_numero)

    # Rookie year
    try:
        rookie_year = soup.find('h2', string=re.compile(r'joined the LPGA Tour in \d{4}'))
        match = re.search(r'joined the LPGA Tour in (\d{4})', rookie_year.text)
        rookie = int(match.group(1))
    except:
        rookie = "-"
    print('Rookie year: ' + str(rookie))
    rookie_year_perf.append(rookie)

    # Imagen
    try:
        img_tag = soup.find('img', src=re.compile(r"/-/media/images/(lpga|epson-tour)/players/"))
        if img_tag:
            foto_jugadora = "https://www.lpga.com" + img_tag['src']
        else:
            foto_jugadora = None
    except Exception as e:
        print(f"Error buscando imagen: {e}")
        foto_jugadora = None

    # Descargar imagen
    if foto_jugadora:
        img_url_perf.append(foto_jugadora)
        try:
            img_response = req.get(foto_jugadora, stream=True)
            img_response.raise_for_status()
            nombre_archivo = re.sub(r'[\\/*?:"<>|]', "", nombre_completo)
            file_path = os.path.join(carpeta_img_perfil, f"{nombre_archivo}.jpg")
            with open(file_path, "wb") as file:
                for chunk in img_response.iter_content(1024):
                    file.write(chunk)
            print(f"Imagen guardada en: {file_path}")
        except Exception as e:
            print(f"Error al descargar imagen: {e}")
    else:
        img_url_perf.append("No disponible")
        print(f"No se encontró imagen para {nombre_completo}")

    # Guardar CSV (actualizado en cada iteración)
    df_jugador = pd.DataFrame({
        'Jugadora': nombre_perf,
        'Edad': edad_perf,
        'Año inicio LPGA': rookie_year_perf,
        'País': pais_perf,
        'Foto': img_url_perf
    })
    df_jugador.to_csv(csv_informacion_jugador, index=False, sep=';')

driver.quit()
