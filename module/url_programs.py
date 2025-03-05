import json
from winotify import (
    Notification,
    audio
)
from os import (
    system,
    path
)
from subprocess import (
    Popen
)
from threading import (
    Thread
)
from module.info_recycle import (
    check_state_recycle_bin
)

class Programs:
    
    def __init__(self):
        self.flag = 1
        self.hilo_1 = Thread(target=self.open_program)
        self.hilo_2 = Thread(target=self.mostrar_notificacion)
        self.hilo_1.daemon = True
        self.hilo_2.daemon = True
        self.hilo_1.start()
        self.hilo_2.start()
    
    def open_program(self, name_program=None, fullPath=""):
        try:
            if name_program == 'trashbin':
                # Limpia la papelera sin confirmación
                system('PowerShell -Command "Clear-RecycleBin -Confirm:$false"')
                self.mostrar_notificacion()
            else:
                # Construye el path del archivo de configuración
                config_file = path.join(fullPath, "config", "config.json")
                
                if not path.exists(config_file):
                    print(f"Error: {config_file} no encontrado.")
                    return

                # Carga la configuración desde el archivo JSON
                with open(config_file, "r") as r:
                    programs = json.load(r)

                # Verifica si el programa existe en la lista
                if name_program in programs:
                    program = programs[name_program]
                    system(f'start "{program}"')
                else:
                    print(f"Error: {name_program} no se encuentra en la lista de programas.")
        except Exception as e:
            print(f"Ocurrió un error: {e}")
           
           
    def mostrar_notificacion(self):
        notificacion = Notification(
            app_id="Sistema Windows",
            title="Recycle Bin",
            msg="Recycle Bin has been emptied",
            icon="D:\\Fotos\\Iconos_Programas\\trashempty2.png",
            duration="short"
        )
        welcome = Notification(
            app_id="Halloween Wallpaper",
            title="Bienvenido/a 👿",
            msg="Esta será una bonita aventura, jejeje",
            icon="D:\\Fotos\\Iconos_Programas\\trashempty2.png",
            duration="short",
        )
        objetRedes = {
            "Youtube": "https://www.youtube.com/@OnelCrack",
            "Instagram": "https://www.instagram.com/onel_crack/",
            "GitHub": "https://www.github.com/TechOGR"
        }
        for i, v in objetRedes.items():
            welcome.add_actions(label=i, launch=v)
        
        if check_state_recycle_bin and self.flag == 0:
            notificacion.set_audio(audio.SMS,loop=False)
            notificacion.show()
        else:
            welcome.set_audio(audio.SMS,loop=False)
            welcome.show()
            self.flag = 0
            print("No se mostrará la notificación")