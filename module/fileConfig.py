import os
import json

# Nombre del archivo de configuración
config_file = "config.json"

# Función para cargar la configuración
def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
            print("Archivo de configuración cargado.")
            return config
    else:
        print("Archivo de configuración no encontrado. Creando uno nuevo.")
        return {}

# Función para guardar la configuración
def save_config(config):
    with open(config_file, 'w') as file:
        json.dump(config, file, indent=4)
        print("Configuración guardada.")

# Función para agregar un nuevo dato a la configuración
def add_data_to_config(name, address):
    config = load_config()
    config[name] = address
    save_config(config)

# Simulación de agregar datos (esto podría ser reemplazado por la lógica de tu programa)
def main():
    config = load_config()
    
    if not config:
        # Aquí puedes establecer valores predeterminados o dejar que el usuario los introduzca
        name = input("Introduce tu nombre: ")
        address = input("Introduce tu dirección: ")
        add_data_to_config(name, address)
    else:
        # Aquí se usarían los datos cargados del archivo
        print("Datos cargados del archivo de configuración:")
        for name, address in config.items():
            print(f"Nombre: {name}, Dirección: {address}")
        
        # Puedes continuar utilizando estos datos en tu programa según necesites

if __name__ == "__main__":
    main()
