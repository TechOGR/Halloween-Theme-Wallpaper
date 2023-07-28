import ctypes

def is_recycle_bin_empty():
    SHELL32 = ctypes.windll.shell32
    SHQueryRecycleBin = SHELL32.SHQueryRecycleBinW

    # Estructura para almacenar la información de la papelera de reciclaje
    class SHQUERYRBINFO(ctypes.Structure):
        _fields_ = [
            ("cbSize", ctypes.c_ulong),
            ("i64Size", ctypes.c_ulonglong),
            ("i64NumItems", ctypes.c_ulonglong)
        ]

    # Llamada a la función SHQueryRecycleBin para obtener la información de la papelera de reciclaje
    info = SHQUERYRBINFO()
    info.cbSize = ctypes.sizeof(info)
    result = SHQueryRecycleBin(None, ctypes.byref(info))

    if result == 0:
        # La función se ejecutó correctamente
        if info.i64NumItems > 0:
            return False  # La papelera de reciclaje no está vacía
        else:
            return True  # La papelera de reciclaje está vacía
    else:
        # Ocurrió un error al llamar a la función
        raise OSError("Error al obtener el estado de la papelera de reciclaje")

# Ejemplo de uso
if is_recycle_bin_empty():
    print("La papelera de reciclaje está vacía")
else:
    print("La papelera de reciclaje no está vacía")