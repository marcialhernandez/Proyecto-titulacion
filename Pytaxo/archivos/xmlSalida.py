try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from clases import alternativa,xmlEntrada
from archivos import nombres
import hashlib, argparse
    
def plantillaGenericaSalida():
    raizXml=ET.Element('plantilla')
    ET.SubElement(raizXml,'enunciado')
    ET.SubElement(raizXml,'opciones')
    return raizXml

def incluyeAlternativas(elementTreeObject,xmlEntradaObject):
    for subRaiz in elementTreeObject.iter():
        if subRaiz.tag=='opciones':
            del subRaiz
    opciones=ET.SubElement(elementTreeObject, 'opciones')
    for conjuntoAlternativas in xmlEntradaObject.permutaAlternativas():
        for alternativa in conjuntoAlternativas:
            opcion = ET.SubElement(opciones, 'alternativa',puntaje=alternativa.puntaje,id=alternativa.llave,tipo=alternativa.tipo)
            opcion.text=alternativa.glosa
            hijo=ET.SubElement(opcion, 'comentario')
            hijo.text=alternativa.comentario
        print ET.tostring(elementTreeObject, 'utf-8', method="xml")

def agregaAlternativa(listaAlternativas,alternativaAAgregar,largoMax):
    if len(listaAlternativas)==largoMax:
        return 0
    for alternativa in listaAlternativas:
        if alternativa.llave==alternativaAAgregar.llave:
            return False
    listaAlternativas.append(alternativaAAgregar)
    return True

def despejaAlternativas(conjuntoAlternativas):
    listaLlaves=list()
    for alternativa in conjuntoAlternativas:
        if alternativa.llave in listaLlaves:
            return False
        else:
            listaLlaves.append(alternativa.llave)
    return True

def validaConjuntoAlternativas(conjuntoAlternativas):
    indicaExistenciaRespuesta=False
    for alternativa in conjuntoAlternativas:
        if alternativa.tipo=='solucion':
            indicaExistenciaRespuesta=True
    if indicaExistenciaRespuesta==True:
        return True
    else:
        return False

def analizaTipoDefinicion(subRaiz):
    pass

def analizaTipoEnunciadoIncompleto(subRaiz):
    pass

def preguntaParser(raizXmlEntrada,nombreArchivo):
    puntaje=0
    tipo=""
    cantidadAlternativas=0
    conjuntoAlternativas=dict()
    comentarioAlternativa=""
    termino="" #Para el tipo pregunta definicion
    enunciado="" #Para el tipo pregunta enunciadoIncompleto
    for subRaiz in raizXmlEntrada.iter('pregunta'):
        puntaje=int((subRaiz.attrib['puntaje']))
        tipo=str(subRaiz.attrib['tipo'])
        cantidadAlternativas=int(subRaiz.attrib['cantidadAlternativas'])
    if tipo=='definicion':
        for subRaiz in raizXmlEntrada.iter('termino'):
            termino=subRaiz.text
    if tipo=='enunciadoIncompleto':
        respuestas=list()
        enunciadoIncompleto=list()
        for subRaiz in raizXmlEntrada.iter('enunciado'):
            for elem in subRaiz:
                if elem.tag=='glosa':
                    enunciadoIncompleto.append(elem.text)
                if elem.tag=='blank':
                    enunciadoIncompleto.append('_'*len(elem.text))
                    respuestas.append(elem.text)
        enunciado=' '.join(enunciadoIncompleto)
        alternativaSolucion=list()
        alternativaSolucion.append(alternativa.alternativa(hashlib.sha256('solucion').hexdigest(),'solucion',str(puntaje),'-'.join(respuestas),comentario='Alternativa Correcta',numeracion=1))
        conjuntoAlternativas[alternativaSolucion[0].llave]=alternativaSolucion
    if tipo=='definicionPareada':
        conjuntoTerminosPareados=dict()
        conjuntoTerminosImpares=dict()
        for subRaiz in raizXmlEntrada.iter('terminos'):
            for glosa in subRaiz.iter('glosa'):
                definicion=glosa.text
                llaveTermino=glosa.attrib['id']
                pozoPares=list()
                pozoImpares=list()
                for par in glosa.iter('par'):
                    pozoPares.append(alternativa.alternativa(llaveTermino,'solucion',str(puntaje),par.text.rstrip()))
                for inpar in glosa.iter('inpar'):
                    textoComentario=""
                    for comentario in inpar.iter('comentario'):
                        textoComentario=textoComentario+' '+comentario.text
                    textoComentario=textoComentario.lstrip()
                    #agrego solo si existe el inpar
                    if bool(inpar.text.rstrip())==True:
                        pozoImpares.append(alternativa.alternativa(llaveTermino,'distractor','0',inpar.text.rstrip()))
                conjuntoTerminosPareados[definicion.rstrip()]=pozoPares
                #No es necesario agregar una llave si no tiene impares
                if len(pozoImpares)>0:
                    conjuntoTerminosImpares[definicion.rstrip()]=pozoImpares
            conjuntoAlternativas['terminos']=conjuntoTerminosPareados
            conjuntoAlternativas['distractores']=conjuntoTerminosImpares
            #print conjuntoAlternativas['terminos'].keys()
    #En la pregunta tipo definicion pareada la arquitectura del conjunto de alternativas cambia
    #ahora es {'terminos':{'definicion':lista de alternativas (las diferentes definiciones)}}
    #{'distractores':{'definicion':lista de distractores (los diferentes distractores)}}
    for subRaiz in raizXmlEntrada.iter('opciones'):
        for opcion in raizXmlEntrada.iter('alternativa'):
            for glosaOpcion in opcion.iter('glosa'):
                comentarioAlternativa=""
                for comentarioGlosa in glosaOpcion.iter('comentario'):
                    comentarioAlternativa=comentarioAlternativa+" "+str(comentarioGlosa.text)
                if opcion.attrib['id'] in conjuntoAlternativas.keys():
                    largoLista=len(conjuntoAlternativas[opcion.attrib['id']])
                    conjuntoAlternativas[opcion.attrib['id']].append(alternativa.alternativa(opcion.attrib['id'],opcion.attrib['tipo'],opcion.attrib['puntaje'],glosaOpcion.text.rstrip(),comentario=comentarioAlternativa,numeracion=largoLista+1))
                else:
                    conjuntoAlternativas[opcion.attrib['id']]=list()
                    conjuntoAlternativas[opcion.attrib['id']].append(alternativa.alternativa(opcion.attrib['id'],opcion.attrib['tipo'],opcion.attrib['puntaje'],glosaOpcion.text.rstrip(),comentario=comentarioAlternativa,numeracion=1))
    return xmlEntrada.xmlEntrada(nombreArchivo,tipo,puntaje,conjuntoAlternativas,cantidadAlternativas,termino=termino,enunciado=enunciado)

#Funcion que analiza argumentos ingresados por comando al ejecutar la funcion
#Retorna la cantidad de alternativas ingresada por el usuario, en caso que no
#se detecte numero alguno ingresado, retorna valor por defecto que es 4
def argParse():
    parser = argparse.ArgumentParser(description='Cantidad de alternativas presentes al momento de generar las preguntas')
    parser.add_argument('-c', required=False,type=int, default=4,
                    help='Especifica la cantidad de alternativas',
                    metavar="CantidadDeAlternativas")
    return parser.parse_args().c

def incrustaAlternativasXml(subRaizOpciones,listaAlternativas):
    #Se concatena el texto de todas las alternativas
    glosasAlternativas=""
    identificadorPregunta=""
    for elem in subRaizOpciones.getchildren():
        subRaizOpciones.remove(elem)
    for alternativa in listaAlternativas:
        identificadorPregunta+=alternativa.identificador()
        opcion = ET.SubElement(subRaizOpciones, 'alternativa')
        opcion.text=alternativa.glosa
        glosasAlternativas+=alternativa.glosa
        opcion.set('puntaje',alternativa.puntaje)
        opcion.set('id',alternativa.llave)
        opcion.set('tipo',alternativa.tipo)
        hijo=ET.SubElement(opcion, 'comentario')
        hijo.text=alternativa.comentario
    #A partir del texto concatenado, se crea una unica ID que representa las alternativas
    #Esta ID se asigna a un nuevo atributo a la subRaiz 'opciones'
    subRaizOpciones.set('id',hashlib.sha256(glosasAlternativas).hexdigest())
    subRaizOpciones.set('idPreguntaGenerada',identificadorPregunta.rstrip())
    pass

#Funcion que analiza cada Xml de entrada
#Si este es de un cierto tipo indicado por la entrada, se parsea con la funcion
#preguntaParser y se agrega a una lista de xmlsFormateadas
#Finalmente retorna esta lista
def lecturaXmls(nombreDirectorioEntradas,tipo):
    listaXmlFormateadas=list()
    for xmlEntrada in nombres.fullEspecificDirectoryNames(nombreDirectorioEntradas):
        arbolXml = ET.ElementTree(file=xmlEntrada)
        raizXml=arbolXml.getroot()
        if raizXml.attrib['tipo']==tipo: #'definicion':
            listaXmlFormateadas.append(preguntaParser(raizXml,nombres.obtieneNombreArchivo(xmlEntrada)))
    return listaXmlFormateadas