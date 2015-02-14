#!/usr/bin/env python
# -*- coding: utf-8 -*-
from archivos import nombres
from clases import xmlEntrada
from archivos import acceso
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

# Con esta funcion se obtiene la plantilla del enunciado desde la carpeta plantillas
# Cabe destacar que la plantilla debe tener el mismo nombre este codigo
# Ademas deja el espacion $termino donde se debe reeplazar lo que se desea añadir desde esta pregunta
def lecturaPlantillas(nombreDirectorioPlantillas):
    for archivoPlantilla in nombres.especificDirectoryNames(nombreDirectorioPlantillas):
        if archivoPlantilla=="MC_def_simple"+".xml":
            nombreDirectorioArchivoPlantilla=nombres.directorioReal(nombreDirectorioPlantillas+"/MC_def_simple"+".xml")
            arbolXml=ET.ElementTree(file=nombreDirectorioArchivoPlantilla)
            enunciadoSinTermino=""
            for elem in arbolXml.iter():
                if elem.tag=='enunciado':
                    enunciadoSinTermino=enunciadoSinTermino+' '+elem.text
                if elem.tag=='termino':
                    enunciadoSinTermino=enunciadoSinTermino+' '+'$termino'
            return enunciadoSinTermino.encode("ascii","ignore")
        #.translate(dict.fromkeys(map(ord, u",!.;¿?")))
    return False

# Declaracion de directorio de entradas
nombreDirectorioEntradas="./Entradas/Definiciones"
nombreDirectorioPlantillas="./Plantillas"
nombreCompilador="python"
listaXmlEntrada=list()

# Almacenamiento usando el parser para este tipo de pregunta
if nombres.validaExistenciasSubProceso(nombreDirectorioEntradas)==True:
    listaXmlEntrada=lecturaXmls(nombreDirectorioEntradas)

listaXmlEntrada[0].preguntaDefSimpleIntoXml()
print lecturaPlantillas(nombreDirectorioPlantillas) 
# Validacion de guardado de la informacion de todos los archivos xml de entrada de
#forma correcta.

# for elem in listaXmlEntrada:
#     elem.printContenidoEntrada()