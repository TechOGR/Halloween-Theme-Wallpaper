from os import path
import os
from flask import (
    json,
    render_template,
    request, 
    send_from_directory
)
from module.info_recycle import check_state_recycle_bin
from module.sonidos import sonido_bruja, sonido_grito, sonido_error

def rutas(app, nombre_programa, instance_programs, full_path):
    # Ruta para exponer las imágenes
    @app.route("/img/<path:filename>")
    def render_img(filename):
        return send_from_directory("static/img", filename)
    
    # Ruta principal de inicio
    @app.route("/")
    def index():            
        return render_template("index.html")
    
    # Ruta para abrir un programa
    @app.route("/open", methods=["POST"])
    def open_programs():
        name_program = request.json.get("name")
        if not name_program:
            return json.jsonify({"error": "No program name provided"}), 400
        
        try:
            instance_programs.open_program(name_program)
            return json.jsonify({"status": "Program opened successfully"}), 200
        except Exception as e:
            return json.jsonify({"error": str(e)}), 500
    
    # Función que devuelve el estado de la papelera
    def get_value_file():
        return check_state_recycle_bin()
    
    # Ruta que da el estado de la papelera de reciclaje
    @app.route("/obtener_valor")
    def get_value():
        return json.jsonify({"valor": get_value_file()})
    
    # Ruta que manda a sonar un sonido
    @app.route("/sonar", methods=["POST"])
    def sonar():
        data = request.json.get("valor")
        if data == "suena":
            sonido_bruja(full_path)
        elif data == "grito":
            sonido_grito(full_path)
        else:
            return json.jsonify({"error": "Invalid sound"}), 400
            
        return "ok"
    
    # Ruta para obtener el valor del susto
    @app.route("/get_fear")
    def get_fear():
        try:
            with open(path.join(full_path, "archivo.txt"), "r") as file:
                data = file.readline().strip()
            
            if data == "Activar":
                datos = {"value": data}
                with open(path.join(full_path, "archivo.txt"), "w") as file:
                    file.write("")
                return json.jsonify(datos)
            else:
                return json.jsonify({"value": "error"})
        except FileNotFoundError:
            return json.jsonify({"error": "File not found"}), 404
        except Exception as e:
            return json.jsonify({"error": str(e)}), 500
    
    # Ruta para obtener el estado del servidor
    @app.route("/getStatusServer")
    def retornStatus():
        return json.jsonify({"Name": "Onel Crack"})
    
    @app.route("/load_programs")
    def loadPrograms():
        return {"Good", "Hola"}