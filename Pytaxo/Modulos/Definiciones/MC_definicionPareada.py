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

#No preserva el orden    
def quitaDuplicados(seq):
    return {}.fromkeys(seq).keys()
    
def retornaSignificadoCadena(cadenaSimbolos,xmlEntradaObject,distractores,solucion,cantidadAlternativas):
    listaCombinatoria=list()
    listaConjuntoAlternativas=list()
    if '+' in cadenaSimbolos:
        for simbolos in quitaDuplicados(cadenaSimbolos.split('+')):
            for conjunto in retornaSignificadoSimbolo(simbolos, xmlEntradaObject, distractores, solucion):
                if conjunto not in listaCombinatoria:
                    listaCombinatoria.append(conjunto)
        listaConjuntoDistractores=list(itertools.combinations(listaCombinatoria, cantidadAlternativas))
        if len(listaConjuntoDistractores)>0:
            for conjunto in listaConjuntoDistractores:
            #A cada conjunto generado se le agrega su solucion
                conjunto=list(conjunto)
                conjunto.append(list(solucion))
                listaConjuntoAlternativas.append(conjunto)
        return listaConjuntoAlternativas
    else:
        listaConjuntoDistractores=list(itertools.combinations(retornaSignificadoSimbolo(cadenaSimbolos, xmlEntradaObject, distractores, solucion), cantidadAlternativas))
        if len(listaConjuntoDistractores)>0:
            for conjunto in listaConjuntoDistractores:
                #A cada conjunto generado se le agrega su solucion
                conjunto=list(conjunto)
                conjunto.append(list(solucion))
                listaConjuntoAlternativas.append(conjunto)
        return listaConjuntoAlternativas

def retornaSignificadoSimbolo(simbolo,xmlEntradaObject,distractores,solucion):
    simbolo=simbolo.lstrip().rstrip().lower()
    if simbolo.isdigit()==True:
        if int(simbolo)<=0:
            return list()
        else:
            return pozoDistractoresNesimo(xmlEntradaObject,distractores,int(simbolo),solucion=solucion)
    else:
        return list()

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

#Admite entrada kwuargs[] 'especificacion' de la forma
#2+1 ->alternativas derivadas de distractores con 1 y 2 reemplazos
#1+1 ->alternativas derivadas de distractores con 1 reemplazo (se eliminan repetidos)
#2 ->alternativas derivadas de distractores que tienen si o si 2 reemplazos
#admite n sumas, pero entre más tenga, más recursos utiliza
#ejemplo -> 1+2+3
#0 ->retorna una lista vacia
#0+1 -> genera alternativas derivadas de distractores que tienen si o si 1 reemplazo  
#En caso que no se especifique, genera alternativas correspondientes a la entrada 1+2
#Admite entrada kwuargs[] 'cantidadItems' para limitar cantidad de items generados

def agrupamientoPareado(xmlEntradaObject,solucion,distractores,cantidadAlternativas,**kwuargs):
    if 'especificacion' in kwuargs.keys():
        return retornaSignificadoCadena(kwuargs['especificacion'],xmlEntradaObject,distractores,solucion,cantidadAlternativas)    
    #default ->1+2
    else:
        return retornaSignificadoCadena('1+2',xmlEntradaObject,distractores,solucion,cantidadAlternativas-1)
    #Valida el correcto funcionamiento, reemplazando el return por listaAlternativas
#     print type(listaAlternativas)
#     print len(listaAlternativas)
#     for conjunto in listaAlternativas:
#         print 'conjunto'
#         z=0
#         for elem in conjunto:
#             print str(z)+')'
#             z=+1
#             for elem2 in elem:
#                 print elem2.imprimeAlternativa()            

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
                    for conjuntoDefiniciones in xmlEntradaObject.barajaDefiniciones():
                        #Aqui se presenta cada posible pregunta
                        solucionesYDistractores=posiblesSolucionesYDistractoresConjunto(xmlEntradaObject,conjuntoDefiniciones)
                        #Para cada solucion de la variante actual 
                        for solucion in solucionesYDistractores['soluciones']:
                            
                            #Estos conjunto de alternativas ya tienen su respectiva solucion integrada
                            #Conjuntos de conjuntos de terminos ->tipo lista de lista
                            for cadaConjuntoAlternativas in agrupamientoPareado(xmlEntradaObject,solucion,solucionesYDistractores['distractores'],cantidadAlternativas):
                                
                                #Conjunto de terminos -> tipo lista
                                for cadaAlternativa in cadaConjuntoAlternativas:
                                    #Se requiere convertir las listas de terminos en 1 alternativa!!
                                    idAlternativa=''
                                    comentariosAlternativa=''
                                    glosaAlternativa=''
                                    puntajeAlternativa=0
                                    #Terminos ->tipo alternativa
                                    for cadaTermino in cadaAlternativa:
                                        pass
                                
                                #     for conjunto in listaAlternativas:
#         print 'conjunto'
#         z=0
#         for elem in conjunto:
#             print str(z)+')'
#             z=+1
#             for elem2 in elem:
#                 print elem2.imprimeAlternativa()  
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