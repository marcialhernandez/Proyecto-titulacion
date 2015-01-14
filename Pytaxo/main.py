from archivos import nombres
from archivos import acceso
from clases import item

nombreCarpetaModulo="Modulos"
nombreCompilador="python"
listaModulosDisponibles=list()
#Implica que la carpeta Modulos existe y que ademas contiene modulos para procesar
if nombres.validaCantidadContenido(nombreCarpetaModulo)==True:
    listaModulosDisponibles=nombres.especificDirectoryNames(nombreCarpetaModulo)

for modulo in listaModulosDisponibles:
    modulo=nombreCarpetaModulo+"/"+modulo
    acceso.obtenerResultadosModulo(modulo,nombreCompilador).printModuloPregunta()

#acceso.obtenerResultadosModulo("Modulos/test1.py","python").printModuloPregunta()
#acceso.obtenerResultadosModulo("Modulos/test1.py","python")

#print nombres.validaExistenciaArchivo("Modulos")

#print nombres.currentDirectoryNames()
#nombres.especificDirectoryNames("Modulos")