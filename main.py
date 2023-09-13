from flask import (
    Flask,
    render_template,
    request,
    json,
    send_from_directory
)
from os import (
    path,
    getcwd
)
from pyautogui import (
    hotkey
)
from threading import Thread
from module.url_programs import Programs
from module.info_recycle import check_state_recycle_bin
from module.sonidos import (
    sonido_bruja,
    sonido_grito
)

import socket
import sys

# Clase Principal
class Main:
    
    # Constructor
    def __init__(self):
        
        self.full_path = getcwd()
        self.path_template = path.join(getcwd(),"template")
        self.path_static = path.join(getcwd(),"static")
        print(self.full_path, self.path_template, self.path_static)

        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        self.hilo = Thread(target=self.wait_for_fear)
        self.hilo.daemon = True
        self.hilo.start()
        
        self.app = Flask(__name__, static_folder=self.path_static,template_folder=self.path_template)
        self.nombre_programa = ""
        
        self.rutas()
        
        self.instance_programs = Programs()
        
    def init_server(self):
        self.app.run("localhost",80)
        
    # Definiendo las rutas Webs
    def rutas(self):
        
        # Ruta para exponer las imagenes
        @self.app.route("/img/<path:filename>")
        def render_img(filename):
            return send_from_directory("static/img",filename)
            
        # Ruta Principal de Inicio
        @self.app.route("/")
        def index():            
            return render_template("index.html")
        
        # Ruta a la que se le envia el programa a abrir
        @self.app.route("/open", methods=["POST"])
        def open_programs():
            name_program = request.json["name"]
            
            self.nombre_programa = name_program
            
            self.instance_programs.open_program(name_program)
            
            return "ok";
        
        # Funcion que devuelve el valor de la papelera
        def get_value_file():
            
            if check_state_recycle_bin():
                return True
            else:
                return False
        
        # Ruta que da el estado de la papelera de reciclaje
        @self.app.route("/obtener_valor")
        def get_value():
            
            objeto = {
                "valor": get_value_file()
            }
            
            return json.jsonify(objeto)
          
        # Ruta que manda a sonar
        @self.app.route("/sonar", methods=["POST"])
        def sonar():
            data = request.json["valor"]
            if data == "suena":
                sonido_bruja(self.full_path)
            elif data == "grito":
                sonido_grito(self.full_path)
            else:
                print("nooo")
                
            return "ok"

        # Ruta para obtener el valor del susto
        @self.app.route("/get_fear")
        def get_fear():
            data = open(path.join(self.full_path,"archivo.txt"),"r").readline().strip()
            
            if data == "Activar":
                datos = {
                    "value": data
                }
                open(path.join(self.full_path,"archivo.txt"),"w").write("")
                return json.jsonify(datos)
            else:
               objeto = {
                   "value": "error"
               }
               return json.jsonify(objeto)
            
    # Funcion asíncrona que crea un servidor local con la ip de la interfaz para luego conectarla con la Aplicacion
    def wait_for_fear(self):
        ip = socket.gethostbyname(socket.gethostname())
        
        self.sock.bind((ip, 111))
        self.sock.listen(2)
        
        while True:
            conn, addr = self.sock.accept()
            data = conn.recv(1024).decode("utf-8")
            
            if data.endswith("Activar"):
                open(path.join(self.full_path,"archivo.txt"),"w").write(data[2:])
                hotkey("win", "m")
                
                
# Metodo Main    
if __name__ == "__main__":
    m = Main()
    sys.stdout = open("./stdout.txt", "w")
    m.init_server()