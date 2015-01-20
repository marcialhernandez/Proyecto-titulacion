from archivos import nombres, tipoXml
from clases import xmlEntrada_Def
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

nombreDirectorioEntradas="./Entradas/Definiciones"
nombreCompilador="python"
listaXmlEntrada=list()

if nombres.validaExistenciasSubProceso(nombreDirectorioEntradas)==True:
    listaXmlEntrada=tipoXml.lecturaXmls(nombreDirectorioEntradas)

#Se realiza guardado de la informacion de todos los archivos xml de entrada de
#forma correcta.

# for elem in listaXmlEntrada:
#     elem.printContenidoEntrada()