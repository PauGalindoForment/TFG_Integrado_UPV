import pandas as pd
import ast

# Cargar archivo
ruta = "C:\\NAS_PAU\\TFG\\BBDD_Femenino\\jugadoras.xlsx"
df = pd.read_excel(ruta)

# Contar elementos de la lista en formato string
def contar_elementos(celda):
    try:
        lista = ast.literal_eval(celda)
        if isinstance(lista, list):
            return len(lista)
    except:
        pass
    return 0

# Crear columna nueva
df['n_otros_circuitos'] = df['Otros Tours Jugados'].apply(contar_elementos)

# Guardar el archivo actualizado
df.to_excel(ruta, index=False)

# Verificar resultado
print(df[['Otros Tours Jugados', 'n_otros_circuitos']].head())
