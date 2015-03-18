try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from clases import alternativa,xmlEntrada
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
    conjuntoAlternativas=dict()
    comentarioAlternativa=""
    termino="" #Para el tipo pregunta definicion
    enunciado="" #Para el tipo pregunta enunciadoIncompleto
    for subRaiz in raizXmlEntrada.iter('pregunta'):
        puntaje=int((subRaiz.attrib['puntaje']))
        tipo=str(subRaiz.attrib['tipo'])
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
        alternativaSolucion.append(alternativa.alternativa(hashlib.sha256('solucion').hexdigest(),'solucion',str(puntaje),'-'.join(respuestas),comentario='Alternativa Correcta'))
        conjuntoAlternativas[alternativaSolucion[0].llave]=alternativaSolucion
    for subRaiz in raizXmlEntrada.iter('opciones'):
        for elem in subRaiz:
            comentarioAlternativa=""
            for textoAnexo in elem.iter('comentario'):
                comentarioAlternativa=comentarioAlternativa+" "+textoAnexo.text
                if elem.attrib['id'] in conjuntoAlternativas.keys():
                    conjuntoAlternativas[elem.attrib['id']].append(alternativa.alternativa(elem.attrib['id'],elem.attrib['tipo'],elem.attrib['puntaje'],elem.text.rstrip(),comentario=comentarioAlternativa))
                else:
                    conjuntoAlternativas[elem.attrib['id']]=list()
                    conjuntoAlternativas[elem.attrib['id']].append(alternativa.alternativa(elem.attrib['id'],elem.attrib['tipo'],elem.attrib['puntaje'],elem.text.rstrip(),comentario=comentarioAlternativa))
    for subRaiz in raizXmlEntrada.iter('sustitutos'):
        for elem in subRaiz:
            comentarioAlternativa=""
            for textoAnexo in elem.iter('comentario'):
                comentarioAlternativa=comentarioAlternativa+" "+textoAnexo.text
                if elem.attrib['id'] in conjuntoAlternativas.keys():
                    conjuntoAlternativas[elem.attrib['id']].append(alternativa.alternativa(elem.attrib['id'],elem.attrib['tipo'],elem.attrib['puntaje'],elem.text.rstrip(),comentario=comentarioAlternativa))
                else:
                    pass
    return xmlEntrada.xmlEntrada(nombreArchivo,tipo,puntaje,conjuntoAlternativas,termino=termino,enunciado=enunciado)

#Funcion que analiza argumentos ingresados por comando al ejecutar la funcion
#Retorna la cantidad de alternativas ingresada por el usuario, en caso que no
#se detecte numero alguno ingresado, retorna valor por defecto que es 4
def argParse():
    parser = argparse.ArgumentParser(description='Cantidad de alternativas presentes al momento de generar las preguntas')
    parser.add_argument('-c', required=False,type=int, default=4,
                    help='Especifica la cantidad de alternativas',
                    metavar="CantidadDeAlternativas")
    return parser.parse_args().c

