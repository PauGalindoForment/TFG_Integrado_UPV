from PyPDF2 import PdfReader
import csv

# Ruta del archivo PDF y del archivo csv que se va a generar
pdf_path = "C:\\NAS_PAU\\TFG\\OWGR\\owgr52f2024.pdf"
csv_path = "C:\\NAS_PAU\\TFG\\OWGR\\clasificacion.csv"

# Leer el contenido del PDF
reader = PdfReader(pdf_path)
text = ""
for page in reader.pages:
    text += page.extract_text()

# Procesar el contenido del PDF y extraer las filas
rows = []
header = ["Rank This Week", "Rank Last Week", "End of 2023 Rank", "Name", "Country", 
          "Average Points", "Total Points", "Events Played (Min40-Max52)", 
          "Points Lost", "Points Won", "Actual Events Played"]
rows.append(header)

# Dividir líneas y procesar datos
for line in text.splitlines():
    if line.strip() and line[0].isdigit():  
        parts = line.split() 
        try:
            rank = parts[0]
            last_week = parts[1]
            end_year_rank = parts[2]
            name = " ".join(parts[3:-7]) 
            country = parts[-7]
            avg_points = parts[-6]
            total_points = parts[-5]
            events_played = parts[-4]
            points_lost = parts[-3]
            points_won = parts[-2]
            actual_played = parts[-1]
            
            rows.append([rank, last_week, end_year_rank, name, country, avg_points, 
                         total_points, events_played, points_lost, points_won, actual_played])
        except IndexError:
            continue

# Guardar los datos en un archivo CSV
with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

print(f"Datos guardados en {csv_path}")
