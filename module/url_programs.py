from winotify import (
    Notification,
    audio
)
from subprocess import Popen
from threading import Thread

def open_program(name_program = None):
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
            Popen(["C:\Program Files\JetBrains\IntelliJ IDEA Community Edition 2022.2.3\\bin\\idea64.exe".replace("\\","\\\\")])
        case 'aimp':
            Popen(["C:\Program Files\AIMP\AIMP.exe".replace("\\","\\\\")])
        case 'chrome':
            Popen(["C:\Program Files\Google\Chrome\Application\chrome.exe".replace("\\","\\\\")])
        case 'android':
            Popen(["C:\Program Files\Android\Android Studio\\bin\studio64.exe".replace("\\","\\\\")])
        case 'trashbin':
            Popen(["powershell","-Command", "Clear-RecycleBin", "-Confirm:$false", "-Force"])
            mostrar_notificacion()
        case 'explorer':
            Popen(["explorer.exe"])

flag = 0       
def mostrar_notificacion():
    notificacion = Notification(
        app_id="Sistema Windows",
        title="Recycle Bin",
        msg="Recycle Bin has been emptied",
        icon="D:\\Fotos\\Iconos_Programas\\trashempty2.png",
        duration="short"
    )
    if flag == 1:
        notificacion.set_audio(audio.SMS,loop=False)
        notificacion.show()
    else:
        print("No se mostrará la notificación")
    
hilo_1 = Thread(target=open_program)
hilo_2 = Thread(target=mostrar_notificacion)
hilo_1.daemon = True
hilo_2.daemon = True
hilo_1.start()
hilo_2.start()