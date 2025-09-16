import pandas as pd
import re
import emoji

# Ruta de entrada y salida
input_path = 'C:\\NAS_PAU\\TFG\\BBDD_Unificada\\DatosPublicacionesPGALIV.xlsx'
output_path = 'C:\\NAS_PAU\\TFG\\BBDD_Unificada\\DatosPublicacionesPGALIV2.xlsx'

# Cargar el archivo
df = pd.read_excel(input_path)

# Asegurar que 'texto' es string y sin NaN
df['texto'] = df['texto'].fillna("").astype(str)

# 1. Contar palabras reales (excluye hashtags y menciones)
df['num_palabras'] = df['texto'].apply(
    lambda x: len(re.findall(r'\b(?![#@])\w+\b', x))
)

# 2. Contar hashtags
df['num_hashtags'] = df['texto'].apply(
    lambda x: len(re.findall(r'#\w+', x))
)

# 3. Contar menciones
df['num_menciones'] = df['texto'].apply(
    lambda x: len(re.findall(r'@\w+', x))
)

# 4. Contar emojis
def contar_emojis(texto):
    return sum(1 for char in texto if char in emoji.EMOJI_DATA)

df['num_emojis'] = df['texto'].apply(contar_emojis)

# Guardar resultado
df.to_excel(output_path, index=False)
