import pandas as pd

# Cargar el archivo combinado
file_path = 'C:\\NAS_PAU\\TFG\\PGA\\PGACompleto.xlsx'
file_path2 = 'C:\\NAS_PAU\\TFG\\PGA\\PGACompletoDepurado.xlsx'

df = pd.read_excel(file_path, engine='openpyxl')

# Fusionar las columnas 'instagram__x' e 'instagram_y'
df["Instagram"] = df["Instagram_x"].fillna(df["Instagram_y"])

# Eliminar las columnas antiguas
df.drop(columns=["Instagram_x", "Instagram_y"], inplace=True)

# Guardar el archivo modificado
df.to_excel(file_path2, index=False, engine='openpyxl')

print("Columna 'Instagram' unificada correctamente en 'PGACompletoDepurado.xlsx'")
