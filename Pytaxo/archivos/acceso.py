#!/usr/bin/env python
# -*- coding: utf-8 -*-
from clases import item, entrada
from clases import xmlEntrada
from nombres import obtieneNombreArchivo
import subprocess, stat, os

#Funcion que otorga permisos de acceso a un archivo
#Argumentos:
#-Ruta de archivo y su nombre por ejemplo "Modulos/test1.py"
def permisoAcceso(rutaArchivo):
    st = os.stat(rutaArchivo)
    os.chmod(rutaArchivo, st.st_mode | stat.S_IEXEC)

def formateaResultado(resultado):
    resultado=resultado.split("\n")
    while "" in resultado:
        resultado.remove("")
         
    return resultado
    
#Funcion que ejecuta un modulo creado y obtiene sus resultados
#Argumentos:
#-Ruta de archivo y su nombre por ejemplo "Modulos/test1.py"
#-lenguaje compilador del modulo, por ejemplo "python"
def obtenerResultadosModulo(rutaArchivo, lenguaje):
    permisoAcceso(rutaArchivo)
    proceso = subprocess.Popen([lenguaje, rutaArchivo],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output, errors = proceso.communicate()
    if proceso.returncode:
        try:
            raise Exception(errors)
        except Exception as falla:
            #print type(falla.args)
            #print type(falla.args[0])
            return item.item(obtieneNombreArchivo(rutaArchivo),"",formateaResultado(falla.args[0]))
    else:
        #print output
        return item.item(obtieneNombreArchivo(rutaArchivo),formateaResultado(output),"")

#Funcion que ejecuta una entrada y obtiene sus resultados
#Argumentos:
#-Ruta de archivo y su nombre por ejemplo "Modulos/test1.py"
#-lenguaje compilador del modulo, por ejemplo "python"
def obtenerResultadosEntrada(rutaArchivo, lenguaje):
    permisoAcceso(rutaArchivo)
    proceso = subprocess.Popen([lenguaje, rutaArchivo],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output, errors = proceso.communicate()
    if proceso.returncode:
        try:
            raise Exception(errors)
        except Exception as falla:
            #print type(falla.args)
            #print type(falla.args[0])
            return entrada.entrada(obtieneNombreArchivo(rutaArchivo),"",formateaResultado(falla.args[0]))
    else:
        #print output
        return entrada.entrada(obtieneNombreArchivo(rutaArchivo),formateaResultado(output),"")

#Funcion que retorna un objeto tipo xmlEntrada a partir de la raiz
#obtenida con la biblioteca elementTree
def preguntaDefParser(raizXmlEntrada,nombreArchivo):
    puntaje=0
    termino=""
    definicion=""
    distractores=list()
    for elem in raizXmlEntrada.iter('pregunta'):
        puntaje=int((elem.attrib['puntaje']))
    for elem in raizXmlEntrada.iter('termino'):
        termino=elem.text
    for elem in raizXmlEntrada.iter('definicion'):
        definicion=elem.text
    for elem in raizXmlEntrada.iter('distractor'):
        distractor=list()
        distractor.append(elem.text)
        distractor.append(elem.attrib)
        distractores.append(distractor)
    return xmlEntrada.xmlEntrada(nombreArchivo,puntaje,termino,definicion,distractores)
