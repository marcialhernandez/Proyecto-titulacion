#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import sys
import itertools
from archivos import nombres, xmlSalida
from clases import plantilla
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def posiblesSolucionesYDistractoresConjunto(xmlEntradaObject,conjuntoTerminos):
    salida=dict()
    listaDeListaDeOpciones=list()
    distractores=list()        
    for cadaDefinicion in conjuntoTerminos:
        posiblesTerminos=list()
        for cadaTermino in xmlEntradaObject.alternativas['terminos'][cadaDefinicion]:
            posiblesTerminos.append(cadaTermino)
        listaDeListaDeOpciones.append(posiblesTerminos)
        if cadaDefinicion in xmlEntradaObject.alternativas['distractores'].keys():
            #Con esto se evita errores de intentar acceder a una llave que no existe
            for cadaDistractor in xmlEntradaObject.alternativas['distractores'][cadaDefinicion]:
                distractores.append(cadaDistractor)
    #Se obtiene una lista de posibles soluciones de la variante actual
    salida['soluciones']=list(itertools.product(*listaDeListaDeOpciones))
    salida['distractores']=distractores
    return salida

#def pozoDistractoresNesimo(xmlEntradaObject,solucion,distractores,cantidadDistractores,**kwargs):#cantidadDistractores,pozoNesimo)
def pozoDistractoresNesimo(xmlEntradaObject,distractores,cantidadReemplazoDistractores,**kwargs):#cantidadDistractores,pozoNesimo)
    #Implica que es el primer ciclo
    if 'solucion' in kwargs.keys():
        pozoDistractoresN=list()
        banderaAjustaReemplazos=False
        #Si quiere 0 reemplazos por los distractores, , es la solucion misma
        if cantidadReemplazoDistractores<=0 or len(distractores)==0:
            pozoDistractoresN.append(kwargs['solucion'])
            return pozoDistractoresN
        #Se valida que la cantidad de distractores pedidos puedan ser soportados por los distractores que se piden
        #En caso que no hayan distractores, no se realizara este proceso
        if len(xmlEntradaObject.alternativas['distractores'].keys())<=cantidadReemplazoDistractores:
            cantidadReemplazoDistractores=len(xmlEntradaObject.alternativas['distractores'].keys())
        for cadaDistractor in distractores:
            contador=0
            for cadaTermino in kwargs['solucion']:
                if cadaTermino.llave==cadaDistractor.llave:
                    conjuntoDistractor=list(kwargs['solucion'])
                    conjuntoDistractor[contador]=cadaDistractor
                    if conjuntoDistractor not in pozoDistractoresN:
                        pozoDistractoresN.append(conjuntoDistractor)
                    break
                contador+=1
        cantidadReemplazoDistractores=cantidadReemplazoDistractores-1
        #Se termina recursion 
        if cantidadReemplazoDistractores==0:
            return pozoDistractoresN
        else:
            return pozoDistractoresNesimo(xmlEntradaObject,distractores,cantidadReemplazoDistractores,nuevoPozo=pozoDistractoresN)
    #Implica que es el nesimo ciclo
    if 'nuevoPozo' in kwargs.keys():
        pozoDistractoresD=list()
        for cadaConjunto in kwargs['nuevoPozo']:
            for cadaDistractor in distractores:
                contador=0
                for cadaTermino in cadaConjunto:
                    if cadaTermino.llave==cadaDistractor.llave and cadaTermino.tipo=='solucion':
                        conjuntoDistractor=cadaConjunto[:]
                        conjuntoDistractor[contador]=cadaDistractor
                        if conjuntoDistractor not in pozoDistractoresD:
                            pozoDistractoresD.append(conjuntoDistractor)
                        break
                    contador+=1
        cantidadReemplazoDistractores=cantidadReemplazoDistractores-1
        if cantidadReemplazoDistractores==0:
            return pozoDistractoresD
        else:
            return pozoDistractoresNesimo(xmlEntradaObject,distractores,cantidadReemplazoDistractores,nuevoPozo=pozoDistractoresD)

#No es solucion pues uno de sus terminos es en realidad un distractor
#reemplazar 1 elemento
#de la solucion por 1 de la lista de distractores
#el reemplazo tiene que se por ID, significa que se reemplaza
#un termino por su propio distractor
def pozoDistractoresSingle(xmlEntradaObject,solucion,distractores):
    pozoDistractoresS=list()
    if len(distractores)>=1:
        #En caso que no hayan distractores, no se realizara este proceso
        for cadaDistractor in distractores:
            contador=0
            for cadaTermino in solucion:
                if cadaTermino.llave==cadaDistractor.llave:
                    conjuntoDistractor=list(solucion)
                    conjuntoDistractor[contador]=cadaDistractor
                    if conjuntoDistractor not in pozoDistractoresS:
                        pozoDistractoresS.append(conjuntoDistractor)
                    break
                contador+=1
    return pozoDistractoresS

def pozoDistractoresDouble(xmlEntradaObject,solucion,distractores):
    pozoDistractoresD=list()
    #En caso que no hayan mas de un tipo de distractor, no se realizara este proceso
    if len(xmlEntradaObject.alternativas['distractores'].keys())>1:
        pozoDistractoresS=pozoDistractoresSingle(xmlEntradaObject, solucion, distractores)
        for cadaConjunto in pozoDistractoresS:
            for cadaDistractor in distractores:
                contador=0
                for cadaTermino in cadaConjunto:
                    if cadaTermino.llave==cadaDistractor.llave and cadaTermino.tipo=='solucion':
                        conjuntoDistractor=cadaConjunto[:]
                        conjuntoDistractor[contador]=cadaDistractor
                        if conjuntoDistractor not in pozoDistractoresD:
                            pozoDistractoresD.append(conjuntoDistractor)
                        break
                    contador+=1
    return pozoDistractoresD
        
def agrupamientoPareado(xmlEntradaObject,solucion,distractores,cantidadAlternativas,cantidadDistractoresTerms,**kwuargs):
    if cantidadAlternativas<=1:
        return list()
    tipo=None 
    if len(kwuargs.keys())==0:
        tipo=2
    if tipo==1: #Dificultad 1: Alternativas con 1 distractor
        pass
    elif tipo==2: #Dificultad 2: Alternativas con 1 distractor Mix 2 distractores
        #Esto realiza el mix indicado
        #opciones=itertools.combinations(itertools.chain(pozoDistractoresSingle(xmlEntradaObject,solucion,distractores),pozoDistractoresDouble(xmlEntradaObject,solucion,distractores)),cantidadAlternativas-1)
        for conjunto in pozoDistractoresNesimo(xmlEntradaObject,distractores,cantidadDistractoresTerms,solucion=solucion):
            print '@'
            for lala in conjunto:
                print lala.imprimeAlternativa()
                pass  
        
#         pozoDistractoresSin=pozoDistractoresSingle(xmlEntradaObject,solucion,distractores)
#         pozoDistractoresDou=pozoDistractoresDouble(xmlEntradaObject,solucion,distractores)
#         for conjunto in pozoDistractoresSin:
#             print '@'
#             for lala in conjunto:
#                 print lala.imprimeAlternativa()
#                 pass  
    elif tipo==3: #Dificultad 3: Alternativas con 1 distractor Mix 1 distractor Dislex
        pass
    elif tipo==4: #Dificultad 4: Alternativas con 2 distractores Mix 1 distractor Dislex
        pass
    else:       #Dificutad 5: Alternativas con soluciones Dislex
        pass
    pass
        
        
#     for conjunto in pozoDistractoresDouble:
#         print '@'
#         for lala in conjunto:
#             print lala.imprimeAlternativa()
#     pass                       
    

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

def retornaPlantilla(nombreDirectorioPlantillas,xmlEntradaObject,cantidadAlternativas, tipoPregunta): #,xmlEntradaObject):
    #tipoPregunta=nombres.nombreScript(__file__)
    for plantilla in recogePlantillas(nombreDirectorioPlantillas,tipoPregunta):
        plantillaSalida=xmlSalida.plantillaGenericaSalida()
        for subRaizSalida in plantillaSalida.iter():
                if subRaizSalida.tag=='plantilla':
                    subRaizSalida.set('tipo',xmlEntradaObject.tipo)
                    subRaizSalida.set('id',xmlEntradaObject.id)
#                 if subRaizSalida.tag=='enunciado':
#                     if '@termino' in subRaizSalida.text:
#                         subRaizSalida.text=plantilla.enunciado.replace('@termino',xmlEntradaObject.termino)
                if subRaizSalida.tag=='opciones':
                    for conjuntoTerminos in xmlEntradaObject.barajaDefiniciones():
                        solucionesYDistractores=posiblesSolucionesYDistractoresConjunto(xmlEntradaObject,conjuntoTerminos)
                        #Para cada solucion de la variante actual 
                        for solucion in solucionesYDistractores['soluciones']:
                            print '!!!' 
                            agrupamientoPareado(xmlEntradaObject,solucion,solucionesYDistractores['distractores'],cantidadAlternativas,5)
#                     for conjuntoAlternativas in xmlEntradaObject.agrupamientoAlternativas2(cantidadAlternativas):
#                         xmlSalida.incrustaAlternativasXml(subRaizSalida, conjuntoAlternativas)
#                         print ET.tostring(plantillaSalida, 'utf-8', method="xml")
    pass

# Declaracion de directorio de entradas
nombreDirectorioEntradas="./Entradas/Definiciones"
nombreDirectorioPlantillas="./Plantillas"
nombreCompilador="python"
tipoPregunta='definicionPareada'
listaXmlEntrada=list()

# Almacenamiento usando el parser para este tipo de pregunta

#Ahora la entrada que indica la cantidad de alternativas viene incrustada como atributo en los respectivos
#XML de entrada
#cantidadAlternativas=xmlSalida.argParse()

if nombres.validaExistenciasSubProceso(nombreDirectorioEntradas)==True:
    listaXmlEntrada=xmlSalida.lecturaXmls(nombreDirectorioEntradas, tipoPregunta)
    
for cadaXmlEntrada in listaXmlEntrada:
    retornaPlantilla(nombreDirectorioPlantillas, cadaXmlEntrada, cadaXmlEntrada.cantidadAlternativas,tipoPregunta)