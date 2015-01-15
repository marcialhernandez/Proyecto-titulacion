from archivos import nombres
from archivos import acceso

nombreCarpetaModulo="codigoEntrada"
nombreCompilador="python"
listaEntradasDisponibles=list()
#Implica que la carpeta Modulos existe y que ademas contiene modulos para procesar
if nombres.validaCantidadContenido(nombreCarpetaModulo)==True:
    listaModulosDisponibles=nombres.especificDirectoryNames(nombreCarpetaModulo)

for modulo in listaModulosDisponibles:
    modulo=nombreCarpetaModulo+"/"+modulo
    acceso.obtenerResultadosEntrada(modulo,nombreCompilador).printContenidoEntrada()