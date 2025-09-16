import pandas as pd

# Cargar el archivo CSV generado
df = pd.read_csv("C:\\NAS_PAU\\TFG\\LPGA\\LPGAeventos2024.csv", sep=';')

# Separar país del nombre
df["País"] = df["RANK"].str.extract(r'([A-Z]{2,3})$')         # extrae el país
df["Nombre"] = df["RANK"].str.replace(r'([A-Z]{2,3})$', '', regex=True).str.strip()  # elimina el país del nombre

# Reordenar columnas
df = df[["Nombre", "País", "ATHLETE"]]

# Guardar el nuevo CSV
df.to_csv("C:\\NAS_PAU\\TFG\\LPGA\\LPGAeventos2024_separado.csv", index=False, sep=';', encoding='utf-8-sig')
print("País y nombre separados correctamente.")
