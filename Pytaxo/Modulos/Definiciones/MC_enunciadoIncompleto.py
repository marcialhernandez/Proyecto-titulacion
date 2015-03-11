#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import sys
from archivos import nombres, xmlSalida
from clases import xmlEntrada
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

#Funcion que retorna un objeto tipo xmlEntrada a partir de un
#xml enfocado a completar un enunciado
def preguntaEnunciadoIncompletoParser(raizXmlEntrada,nombreArchivo):
    puntaje=0
    tipo=""
    enunciadoIncompleto=list()
    respuestas=list()
    distractores=list()
    for elem in raizXmlEntrada.iter('pregunta'):
        puntaje=int((elem.attrib['puntaje']))
        tipo=str(elem.attrib['tipo'])
    for subRaiz in raizXmlEntrada:
        if subRaiz.tag=='enunciado':
            enunciadoIncompleto.append(subRaiz.text)
        if subRaiz.tag=='blank':
            enunciadoIncompleto.append('______')
            respuestas.append(subRaiz.text)
    for elem in raizXmlEntrada.iter('distractor'):
        distractor=list()
        distractor.append(elem.text)
        distractor.append(elem.attrib)
        distractores.append(distractor)
    return xmlEntrada.xmlEntrada(nombreArchivo,tipo,puntaje,distractores,enunciadoIncompleto=enunciadoIncompleto,respuestas=respuestas)

#Funcion que analiza cada Xml de entrada
#Si este es de tipo enunciadoIncompleto, se parsea con la funcion
#preguntaEnunciadoIncompletoParser y se añade a una lista de xmlsFormateadas
#Finalmente retorna esta lista
def lecturaXmls(nombreDirectorioEntradas):
    listaXmlFormateadas=list()
    for xmlEntrada in nombres.fullEspecificDirectoryNames(nombreDirectorioEntradas):
        arbolXml = ET.ElementTree(file=xmlEntrada)
        raizXml=arbolXml.getroot()
        if raizXml.attrib['tipo']=='enunciadoIncompleto':
            listaXmlFormateadas.append(preguntaEnunciadoIncompletoParser(raizXml,nombres.obtieneNombreArchivo(xmlEntrada)))
    
    return listaXmlFormateadas

#Funcion que crea una nueva plantilla que corresponde a este tipo de pregunta
#añadiendo los datos obtenidos desde la entrada de
#su mismo tipo, luego una vez completada la pregunta, se imprime
#por pantalla para que la informacion pueda ser recogida por el programa
#principal
def retornaPlantilla(xmlEntradaObject): #,xmlEntradaObject):
    raizXml=xmlSalida.plantillaGenericaSalida()
    for subRaiz in raizXml.iter():
        if subRaiz.tag==('plantilla'):
            subRaiz.set('tipo',xmlEntradaObject.tipo)
        if subRaiz.tag==('enunciado'):
            subRaiz.set('last',"true")
            subRaiz.text=xmlEntradaObject.retornaEnunciadoIncompleto()
        if subRaiz.tag==('opciones'):
            for alternativa in xmlEntradaObject.retornaAlternativas():
                subRaizAlternativa=ET.SubElement(subRaiz,'alternativa')
                subRaizAlternativa.text=alternativa[0]
                subRaizAlternativa.set('ponderacion',str(alternativa[1]['ponderacion']))
    ET.dump(raizXml)
    #raizXml.write(sys.stdout,pretty_print=True)                
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
    retornaPlantilla(cadaXmlEntrada)