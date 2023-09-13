from winotify import (
    Notification,
    audio
)
from os import (
    system
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
    
    def open_program(self,name_program = None):
        
        match name_program:
            case 'qt_designer':
                Popen(["C:\Program Files (x86)\Qt Designer\\designer.exe".replace("\\","\\\\")])
            case 'figma':
                Popen(["C:\\Users\\guila\\AppData\\Local\\Figma\\app-116.8.5\\Figma.exe"])
            case 'hide':
                Popen(["C:\Program Files (x86)\\hide.me VPN\Hide.me.exe".replace("\\","\\\\")])
            case 'vscode':
                Popen(["C:\\Users\\guila\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"])
            case 'idea':
                Popen(["C:\\Program Files\\JetBrains\\IntelliJ IDEA Community Edition 2023.2\\bin\\idea64.exe".replace("\\","\\\\")])
            case 'aimp':
                Popen(["C:\Program Files\AIMP\AIMP.exe".replace("\\","\\\\")])
            case 'chrome':
                Popen(["C:\Program Files\Google\Chrome\Application\chrome.exe".replace("\\","\\\\")])
            case 'android':
                Popen(["C:\Program Files\Android\Android Studio\\bin\studio64.exe".replace("\\","\\\\")])
            case 'trashbin':
                # Popen(["powershell","-Command", "Clear-RecycleBin", "-Confirm:$false", "-Force"])
                system("rd /s /q C:\\$Recycle.Bin")
                self.mostrar_notificacion()
            case 'blender':
                Popen(["C:\Program Files\Blender Foundation\Blender 3.6\\blender-launcher.exe".replace("\\","\\\\")])
            case 'U_F':
                Popen(["C:\\Users\\guila\\AppData\\Local\\Programs\\Up_Local_Cloud_Down\\Upload_Files.exe"])
            case 'tunes':
                Popen(["C:\Program Files\iTunes\\iTunes.exe".replace("\\","\\\\")])
            case 'explorer':
                Popen(["explorer.exe"])

    
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
            title="Bienvenida 👿",
            msg="Bienvenido al centro de aquí mismo.",
            icon="D:\\Fotos\\Iconos_Programas\\trashempty2.png",
            duration="short"
        )
        
        if check_state_recycle_bin and self.flag == 0:
            notificacion.set_audio(audio.SMS,loop=False)
            notificacion.show()
        else:
            welcome.set_audio(audio.SMS,loop=False)
            welcome.show()
            self.flag = 0
            print("No se mostrará la notificación")