from archivos import nombres
from archivos import acceso

nombreDirectorioEntradas="./Entradas/Codigo"
nombreCompilador="python"

if nombres.validaExistenciasSubProceso(nombreDirectorioEntradas)==True:
    for codigoEntrada in nombres.fullEspecificDirectoryNames(nombreDirectorioEntradas):
        acceso.obtenerResultadosEntrada(nombres.directorioReal(codigoEntrada),nombreCompilador).printContenidoEntrada()
        #Aqui se debe dar comienzo por obtener los datos de cada xml en vez de procesarlos como subproceso
