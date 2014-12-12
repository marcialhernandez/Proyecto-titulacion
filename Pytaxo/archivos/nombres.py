import os

#Funcion que retorna lista con los nombres de los archivos/carpetas del
#directorio actual
def currentDirectoryNames():
    listaDirectorios=list()
    for dirname, dirnames, filenames in os.walk('.'):
    # print path to all subdirectories first.
        for subdirname in dirnames:
            listaDirectorios.append(subdirname)
            #print os.path.join(dirname, subdirname)
    return listaDirectorios

def currentSubdirectoyNames():
    for dirname, dirnames, filenames in os.walk('.'):
    # print path to all subdirectories first.
    # print path to all filenames.
        for filename in filenames:
            print os.path.join(dirname, filename)
    pass

def especificDirectoryNames(nombreArchivo):
    listaDirectorios=list()
    for dirname, dirnames, filenames in os.walk(nombreArchivo):
        for filename in filenames:
            listaDirectorios.append(filename)
            #print os.path.join(dirname, filename)
    return listaDirectorios

def validaExistenciaArchivo(nombreArchivo):
    listaDirectorios=currentDirectoryNames()
    estado=False
    for nombre in listaDirectorios:
        if nombre==nombreArchivo:
            estado=True
    if estado==False:
        mensaje= "Sistema: No existe el archivo '" +nombreArchivo +"'"
        print (mensaje)
    return estado

def validaCantidadContenido(nombreCarpeta):
    estado=validaExistenciaArchivo(nombreCarpeta)
    if estado==False:
        return estado
    
    listaDirectorios=especificDirectoryNames(nombreCarpeta)
    if len(listaDirectorios)==0:
        mensaje="La carpeta '" +nombreCarpeta +"'  no contiene modulos para procesar"
        print (mensaje)
        estado=False
    return estado

#Funcion que obtiene nombre de archivo
#Argumento:
#string que representa ruta de archivo, ejemplo: "Modulos/test1.py"
def obtieneNombreArchivo(rutaArchivo):
    nombre=""
    if '/' in rutaArchivo:
        cadena=rutaArchivo.split("/")
        largoCadena=len(cadena)-1
        nombre=cadena[largoCadena]
    else:
        nombre=rutaArchivo
    nombre=nombre.replace(".py","")
    return nombre
        
    