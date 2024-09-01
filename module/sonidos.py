import sounddevice as sd
import soundfile as sf
from os import path


def sonido_bruja(main_dir):
    path_sonido = path.join(main_dir, "sounds","bruja.mp3")
    
    data, rates = sf.read(path_sonido)
    
    sd.play(data,rates)
    sd.wait()
    
def sonido_grito(main_dir):

    path_sonido = path.join(main_dir, "sounds","grito.mp3")
    
    data, rates = sf.read(path_sonido)
    
    sd.play(data,rates)
    sd.wait()