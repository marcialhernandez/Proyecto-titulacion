#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import sys
from archivos import nombres, xmlSalida
from clases import xmlEntrada, alternativa
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import argparse, hashlib


def lecturaXmls(nombreDirectorioEntradas,tipo):
    listaXmlFormateadas=list()
    for xmlEntrada in nombres.fullEspecificDirectoryNames(nombreDirectorioEntradas):
        arbolXml = ET.ElementTree(file=xmlEntrada)
        raizXml=arbolXml.getroot()
        if raizXml.attrib['tipo']==tipo:
            listaXmlFormateadas.append(xmlSalida.preguntaParser(raizXml,nombres.obtieneNombreArchivo(xmlEntrada)))
    
    return listaXmlFormateadas

#Funcion que crea una nueva plantilla que corresponde a este tipo de pregunta
#añadiendo los datos obtenidos desde la entrada de
#su mismo tipo, luego una vez completada la pregunta, se imprime
#por pantalla para que la informacion pueda ser recogida por el programa
#principal
def retornaPlantilla(nombreDirectorioPlantillas,xmlEntradaObject,cantidadAlternativas): #,xmlEntradaObject):
    tipoPregunta=nombres.nombreScript(__file__)
    #for plantilla in recogePlantillas(nombreDirectorioPlantillas,tipoPregunta):
    plantillaSalida=xmlSalida.plantillaGenericaSalida()
    for subRaizSalida in plantillaSalida.iter():
            if subRaizSalida.tag=='plantilla':
                subRaizSalida.set('tipo',xmlEntradaObject.tipo)
                subRaizSalida.set('id',xmlEntradaObject.id)
            if subRaizSalida.tag=='enunciado':
                subRaizSalida.text=xmlEntradaObject.enunciado
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
tipoPregunta="enunciadoIncompleto"
listaXmlEntrada=list()

cantidadAlternativas=xmlSalida.argParse()

if nombres.validaExistenciasSubProceso(nombreDirectorioEntradas)==True:
    listaXmlEntrada=lecturaXmls(nombreDirectorioEntradas, tipoPregunta)

for cadaXmlEntrada in listaXmlEntrada:
    retornaPlantilla(nombreDirectorioPlantillas, cadaXmlEntrada, cantidadAlternativas)

# # Almacenamiento usando el parser para este tipo de pregunta
# if nombres.validaExistenciasSubProceso(nombreDirectorioEntradas)==True:
#     listaXmlEntrada=lecturaXmls(nombreDirectorioEntradas)
# 
# for cadaXmlEntrada in listaXmlEntrada:
#     retornaPlantilla(cadaXmlEntrada)