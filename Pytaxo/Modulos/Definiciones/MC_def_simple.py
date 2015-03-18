#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import sys
from archivos import nombres, xmlSalida
from clases import xmlEntrada, alternativa, plantilla
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import argparse, hashlib

#Funcion que analiza cada Xml de entrada
#Si este es de un cierto tipo indicado por la entrada, se parsea con la funcion
#preguntaParser y se añade a una lista de xmlsFormateadas
#Finalmente retorna esta lista
def lecturaXmls(nombreDirectorioEntradas,tipo):
    listaXmlFormateadas=list()
    for xmlEntrada in nombres.fullEspecificDirectoryNames(nombreDirectorioEntradas):
        arbolXml = ET.ElementTree(file=xmlEntrada)
        raizXml=arbolXml.getroot()
        if raizXml.attrib['tipo']==tipo: #'definicion':
            listaXmlFormateadas.append(xmlSalida.preguntaParser(raizXml,nombres.obtieneNombreArchivo(xmlEntrada)))
    
    return listaXmlFormateadas

#Funcion que analiza la plantilla que corresponde a este tipo de pregunta
#A esa plantilla se le añaden los datos obtenidos desde la entrada de
#su mismo tipo, luego una vez completada la pregunta, se imprime
#por pantalla para que la informacion pueda ser recogida por el programa
#principal

def recogePlantillas(nombreDirectorioPlantillas,tipoPregunta):
    validaPlantilla=False
    plantillasValidas=list()
    for archivoPlantilla in nombres.especificDirectoryNames(nombreDirectorioPlantillas):
        nombreDirectorioArchivoPlantilla=nombres.directorioReal(nombreDirectorioPlantillas+"/"+archivoPlantilla)
        arbolXmlPlantillaEntrada = ET.ElementTree() # instantiate an object of *class* `ElementTree`
        arbolXmlPlantillaEntrada.parse(nombreDirectorioArchivoPlantilla)
        #arbolXml=ET.ElementTree(file=nombreDirectorioArchivoPlantilla)
        for subRaiz in arbolXmlPlantillaEntrada.iter('plantilla'):
            if subRaiz.attrib['tipo']==tipoPregunta:
                validaPlantilla=True
                     
        if validaPlantilla==True:
            enunciado=""
            for subRaiz in arbolXmlPlantillaEntrada.iter():
                if subRaiz.tag=='glosa':
                    enunciado=enunciado+subRaiz.text
                if subRaiz.tag=='termino':
                    enunciado=enunciado+' @termino'
            #plantillasValidas.append(arbolXmlPlantillaEntrada)
            plantillasValidas.append(plantilla.plantilla(tipoPregunta,enunciado.rstrip()))
    return plantillasValidas
    
def retornaPlantilla(nombreDirectorioPlantillas,xmlEntradaObject,cantidadAlternativas): #,xmlEntradaObject):
    tipoPregunta=nombres.nombreScript(__file__)
    for plantilla in recogePlantillas(nombreDirectorioPlantillas,tipoPregunta):
        plantillaSalida=xmlSalida.plantillaGenericaSalida()
        for subRaizSalida in plantillaSalida.iter():
                if subRaizSalida.tag=='plantilla':
                    subRaizSalida.set('tipo',xmlEntradaObject.tipo)
                    subRaizSalida.set('id',xmlEntradaObject.id)
                if subRaizSalida.tag=='enunciado':
                    subRaizSalida.text=plantilla.enunciado.replace('@termino',xmlEntradaObject.termino)
                if subRaizSalida.tag=='opciones':
                    for conjuntoAlternativas in xmlEntradaObject.agrupamientoAlternativas(cantidadAlternativas):
                        #Se concatena el texto de todas las alternativas
                        glosasAlternativas=""
                        for elem in subRaizSalida.getchildren():
                            subRaizSalida.remove(elem)
                        for alternativa in conjuntoAlternativas:
                            opcion = ET.SubElement(subRaizSalida, 'alternativa')
                            opcion.text=alternativa.glosa
                            glosasAlternativas+=alternativa.glosa
                            opcion.set('puntaje',alternativa.puntaje)
                            opcion.set('id',alternativa.llave)
                            opcion.set('tipo',alternativa.tipo)
                            hijo=ET.SubElement(opcion, 'comentario')
                            hijo.text=alternativa.comentario
                        #A partir del texto concatenado, se crea una unica ID que representa las alternativas
                        #Esta ID se asigna a un nuevo atributo a la subRaiz 'opciones'
                        subRaizSalida.set('id',hashlib.sha256(glosasAlternativas).hexdigest())
                        print ET.tostring(plantillaSalida, 'utf-8', method="xml")
    pass

# Declaracion de directorio de entradas
nombreDirectorioEntradas="./Entradas/Definiciones"
nombreDirectorioPlantillas="./Plantillas"
nombreCompilador="python"
tipoPregunta='definicion'
listaXmlEntrada=list()

# Almacenamiento usando el parser para este tipo de pregunta

cantidadAlternativas=xmlSalida.argParse()

if nombres.validaExistenciasSubProceso(nombreDirectorioEntradas)==True:
    listaXmlEntrada=lecturaXmls(nombreDirectorioEntradas, tipoPregunta)

for cadaXmlEntrada in listaXmlEntrada:
    retornaPlantilla(nombreDirectorioPlantillas, cadaXmlEntrada, cantidadAlternativas)

#La forma para quitar los signos que no fueron pasados correctamente desde
#la entrada es la siguiente
# enunciadoSinTermino.encode("ascii","ignore")
#         #.translate(dict.fromkeys(map(ord, u",!.;¿?")))