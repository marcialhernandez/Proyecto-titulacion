#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import sys
from archivos import nombres
from clases import xmlEntrada
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

#Funcion que retorna un objeto tipo xmlEntrada a partir de un
#xml enfocado a definir un termino
def preguntaDefParser(raizXmlEntrada,nombreArchivo):
    puntaje=0
    tipo=""
    termino=""
    definicion=""
    distractores=list()
    for elem in raizXmlEntrada.iter('pregunta'):
        puntaje=int((elem.attrib['puntaje']))
        tipo=str(elem.attrib['tipo'])
    for elem in raizXmlEntrada.iter('termino'):
        termino=elem.text
    for elem in raizXmlEntrada.iter('definicion'):
        definicion=elem.text
    for elem in raizXmlEntrada.iter('distractor'):
        distractor=list()
        distractor.append(elem.text)
        distractor.append(elem.attrib)
        distractores.append(distractor)
    return xmlEntrada.xmlEntrada(nombrePregunta=nombreArchivo,tipo=tipo,puntaje=puntaje,termino=termino,definicion=definicion,distractores=distractores)

#Funcion que analiza cada Xml de entrada
#Si este es de tipo Definicion, se parsea con la funcion
#preguntaDefParser y se añade a una lista de xmlsFormateadas
#Finalmente retorna esta lista
def lecturaXmls(nombreDirectorioEntradas):
    listaXmlFormateadas=list()
    for xmlEntrada in nombres.fullEspecificDirectoryNames(nombreDirectorioEntradas):
        arbolXml = ET.ElementTree(file=xmlEntrada)
        raizXml=arbolXml.getroot()
        if raizXml.attrib['tipo']=='definicion':
            listaXmlFormateadas.append(preguntaDefParser(raizXml,nombres.obtieneNombreArchivo(xmlEntrada)))
    
    return listaXmlFormateadas

#Funcion que analiza la plantilla que corresponde a este tipo de pregunta
#A esa plantilla se le añaden los datos obtenidos desde la entrada de
#su mismo tipo, luego una vez completada la pregunta, se imprime
#por pantalla para que la informacion pueda ser recogida por el programa
#principal
def retornaPlantilla(nombreDirectorioPlantillas,xmlEntradaObject): #,xmlEntradaObject):
    nombrePlantillaCorrespondiente=nombres.nombreScript(__file__)+".xml"
    for archivoPlantilla in nombres.especificDirectoryNames(nombreDirectorioPlantillas):
        if archivoPlantilla==nombrePlantillaCorrespondiente:
            nombreDirectorioArchivoPlantilla=nombres.directorioReal(nombreDirectorioPlantillas+"/"+nombrePlantillaCorrespondiente)
            arbolXml=ET.ElementTree(file=nombreDirectorioArchivoPlantilla)
            for subRaiz in arbolXml.iter():
                if subRaiz.tag=='plantilla':
                    subRaiz.set('tipo',xmlEntradaObject.tipo)
                if subRaiz.tag=='termino':
                    subRaiz.text=xmlEntradaObject.termino
                if subRaiz.tag=='enunciado' and subRaiz.attrib['last']=="true":
                    for alternativa in xmlEntradaObject.retornaAlternativas():
                        opcion = ET.SubElement(subRaiz, 'alternativa')
                        opcion.text=alternativa[0]
                        opcion.set('ponderacion',str(alternativa[1]['ponderacion']))
    ET.dump(arbolXml)
    #arbolXml.write(sys.stdout)   
    pass

# Declaracion de directorio de entradas
nombreDirectorioEntradas="./Entradas/Definiciones"
nombreDirectorioPlantillas="./Plantillas"
nombreCompilador="python"
listaXmlEntrada=list()

# Almacenamiento usando el parser para este tipo de pregunta
if nombres.validaExistenciasSubProceso(nombreDirectorioEntradas)==True:
    listaXmlEntrada=lecturaXmls(nombreDirectorioEntradas)

for cadaXmlEntrada in listaXmlEntrada:
    retornaPlantilla(nombreDirectorioPlantillas, cadaXmlEntrada)

#La forma para quitar los signos que no fueron pasados correctamente desde
#la entrada es la siguiente
# enunciadoSinTermino.encode("ascii","ignore")
#         #.translate(dict.fromkeys(map(ord, u",!.;¿?")))