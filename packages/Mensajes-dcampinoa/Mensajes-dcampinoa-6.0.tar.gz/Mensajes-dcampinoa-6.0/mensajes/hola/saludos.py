import numpy as np #para utilizar numpy con el nombre np

def saludar():
    print("Hola, te saludo desde saludos.saludar()")

def prueba():
    print("Esto es una prueba de la nueva versión 6.0")

def generar_array(numeros):
    #llamar a numpy para generar array
    return np.arange(numeros)


class Saludo:
    def __init__(self):
        print("Hola, te saludo desde Saludos.__init__")

#comprobación para que esto no se llame al importar el archivo en otro 
# print(__name__)
if __name__ == "__main__": #esto devuelve el nombre en clave del fichero
    print(generar_array(5))