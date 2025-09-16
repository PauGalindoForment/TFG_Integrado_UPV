from random import randint
from instagrapi import Client
import pandas as pd
import time

# Iniciar sesión con tus credenciales
cl = Client()
cl.login("#####", "#####")

def buscar_instagram_verificado(nombre):
    """Busca un usuario en Instagram y devuelve su perfil verificado, o el primero si no está verificado."""
    try:
        usuarios = cl.search_users(nombre)
        
        for user in usuarios[:3]:
            user_info = cl.user_info(user.pk)  
            
            if user_info.is_verified: 
                return f"https://www.instagram.com/{user_info.username}"
        
        # Si no se encuentra un verificado, devolver el primero
        if usuarios:
            user_info = cl.user_info(usuarios[0].pk)
            return f"https://www.instagram.com/{user_info.username}"
        
        return "No encontrado"
    
    except Exception as e:
        return f"Error: {str(e)}"

# Cargar archivo Excel con la lista de jugadores
df = pd.read_excel('C:\\NAS_PAU\\TFG\\LPGA\\BuscarInstagram.xlsx')

# Agregar la columna con los perfiles de Instagram verificados
for index, row in df.iterrows():
    nombre = row["Jugadora"]
    df.at[index, "Instagram"] = buscar_instagram_verificado(nombre)
    
    print(f"Procesado: {nombre}")
    # Guardar los resultados en un nuevo Excel
    df.to_excel('C:\\NAS_PAU\\TFG\\LPGA\\BuscarInstagram.xlsx', index=False)

    # Pausa para evitar bloqueos
    time.sleep(randint(10,20))  



print("Completado")
