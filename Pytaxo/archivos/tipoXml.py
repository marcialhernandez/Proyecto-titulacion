from archivos import nombres
from archivos import acceso
from clases import xmlEntrada_Def
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def lecturaXmls(nombreDirectorioEntradas):
    listaXmlFormateadas=list()
    for xmlEntrada in nombres.fullEspecificDirectoryNames(nombreDirectorioEntradas):
        arbolXml = ET.ElementTree(file=xmlEntrada)
        raizXml=arbolXml.getroot()
#       acceso.preguntaDefParser(raizXml,nombres.obtieneNombreArchivo(xmlEntrada)).printContenidoEntrada()
        listaXmlFormateadas.append(acceso.preguntaDefParser(raizXml,nombres.obtieneNombreArchivo(xmlEntrada)))
    
#     for xmlFormateado in listaXmlFormateadas:
#         xmlFormateado.printContenidoEntrada()
    
    return listaXmlFormateadas