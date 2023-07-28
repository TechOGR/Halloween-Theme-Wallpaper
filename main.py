from flask import (
    Flask,
    render_template,
    request,
    json,
    send_from_directory
)
from os import (
    path
)
from threading import Thread
from module.url_programs import open_program
from module.info_recycle import check_state_recycle_bin
from module.check_process import en_ejecucion
from module.sonidos import (
    sonido_bruja,
    sonido_grito
)

import socket


class Main:
    
    def __init__(self):
        self.full_path = path.join(path.dirname(__file__))
        self.path_template = path.join(path.dirname(__file__),"template")
        self.path_static = path.join(path.dirname(__file__),"static")

        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        self.hilo = Thread(target=self.wait_for_fear)
        self.hilo.daemon = True
        self.hilo.start()
        
        self.app = Flask(__name__, static_folder=self.path_static,template_folder=self.path_template)
        self.nombre_programa = ""
        
        self.rutas()
        
    def init_server(self):
        
        self.app.run("localhost",80)
        
    def rutas(self):
        
        @self.app.route("/img/<path:filename>")
        def render_img(filename):
            return send_from_directory("static/img",filename)
            
        @self.app.route("/")
        def index():
            
            return render_template("index.html")
        
        @self.app.route("/open", methods=["POST"])
        def open_programs():
            name_program = request.json["name"]
            
            self.nombre_programa = name_program
            
            open_program(name_program)
            
            return "ok";
        
        def get_value_file():
            
            if check_state_recycle_bin():
                return True
            else:
                return False
        
        @self.app.route("/obtener_valor")
        def get_value():
            
            objeto = {
                "valor": get_value_file()
            }
            
            return json.jsonify(objeto)
          
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
            
        
    def wait_for_fear(self):
        ip = socket.gethostbyname(socket.gethostname())
        
        self.sock.bind((ip, 111))
        self.sock.listen(2)
        
        while True:
            conn, addr = self.sock.accept()
            data = conn.recv(1024).decode("utf-8")
            
            if data.endswith("Activar"):
                open(path.join(self.full_path,"archivo.txt"),"w").write(data[2:])
                
        
if __name__ == "__main__":
    m = Main()
    m.init_server()
    