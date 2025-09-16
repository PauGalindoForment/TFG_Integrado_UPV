import pandas as pd

# Ruta del archivo original
input_path = 'C:\\NAS_PAU\\TFG\\BBDD_Unificada\\DatosPublicacionesPGALIV.xlsx'

# Ruta del archivo de salida
output_path = 'C:\\NAS_PAU\\TFG\\BBDD_Unificada\\DatosPublicacionesPGALIV2.xlsx'

# Cargar el archivo (usa 'latin1' si UTF-8 da error)
df = pd.read_excel(input_path)

# Crear la nueva columna 'nombre_archivo'
df['nombre_archivo'] = df['usuario_instagram'].astype(str) + "_" + df['post'].astype(str) + ".jpg"

# Guardar el resultado
df.to_excel(output_path, index=False)
