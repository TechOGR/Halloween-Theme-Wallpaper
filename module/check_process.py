import subprocess

def en_ejecucion(nombre):
    salida_proceso = str(subprocess.check_output(["tasklist"],shell=True)).lower()
    
    if nombre in salida_proceso:
        return True
    else:
        return False