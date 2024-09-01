from os import path
from flask import (
    json,
    render_template,
    request, 
    send_from_directory
)

from module.info_recycle import check_state_recycle_bin
from module.sonidos import sonido_bruja, sonido_grito


def rutas(app, nombre_programa,instance_programs,full_path):
    # Ruta para exponer las imagenes
    @app.route("/img/<path:filename>")
    def render_img(filename):
        return send_from_directory("static/img",filename)
            
    # Ruta Principal de Inicio
    @app.route("/")
    def index():            
        return render_template("index.html")
        
    # Ruta a la que se le envia el programa a abrir
    @app.route("/open", methods=["POST"])
    def open_programs():
        name_program = request.json["name"]
        
        nombre_programa = name_program
        
        instance_programs.open_program(name_program)
        
        return "ok";
    
    # Funcion que devuelve el valor de la papelera
    def get_value_file():
        
        if check_state_recycle_bin():
            return True
        else:
            return False
        
    # Ruta que da el estado de la papelera de reciclaje
    @app.route("/obtener_valor")
    def get_value():
        
        objeto = {
            "valor": get_value_file()
        }
        
        return json.jsonify(objeto)
          
    # Ruta que manda a sonar
    @app.route("/sonar", methods=["POST"])
    def sonar():
        data = request.json["valor"]
        if data == "suena":
            sonido_bruja(full_path)
        elif data == "grito":
            sonido_grito(full_path)
        else:
            print("nooo")
            
        return "ok"

    # Ruta para obtener el valor del susto
    @app.route("/get_fear")
    def get_fear():
        data = open(path.join(full_path,"archivo.txt"),"r").readline().strip()

        if data == "Activar":
            datos = {
                "value": data
            }
            open(path.join(full_path,"archivo.txt"),"w").write("")
            return json.jsonify(datos)
        else:
           objeto = {
               "value": "error"
           }
           return json.jsonify(objeto)
       
    @app.route("/getStatusServer")
    def retornStatus():
        
        response = {
            "Name": "Onel Crack"
        }
        
        return json.jsonify(response)