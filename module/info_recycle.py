import ctypes

def check_state_recycle_bin():
    shell32 = ctypes.windll.shell32
    
    query_recycleBin = shell32.SHQueryRecycleBinW
    
    class rb_info(ctypes.Structure):
        _fields_ = [
            ("cbSize", ctypes.c_ulong),
            ("i64Size", ctypes.c_ulonglong),
            ("i64NumItems", ctypes.c_ulonglong)
        ]
        
    info = rb_info()
    info.cbSize = ctypes.sizeof(info)
    resultado = query_recycleBin(None, ctypes.byref(info))
    
    if resultado == 0:
        
        if info.i64NumItems > 0:
            return False
        else:
            return True
    else:
        raise OSError("Error del Sitema")