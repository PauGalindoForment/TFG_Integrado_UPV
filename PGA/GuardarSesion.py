from instaloader import Instaloader
from instaloader.instaloadercontext import default_user_agent

# Crea instancia
L = Instaloader(save_metadata=False, compress_json=False)
L.context._session.headers['User-Agent'] = default_user_agent()

# Usuario con el que quieres iniciar sesión
#usuario = 'alexremiro789'
#usuario = 'pauupv1'
#usuario = 'pgf220399'
#usuario = 'zaqvho'
#usuario = 'carlosalacaraz22'
usuario = 'federer2203'
# Solicita login y guarda la sesión
L.login(usuario, 'Qwerty88!')
L.save_session_to_file()

print("✅ Sesión guardada correctamente.")
