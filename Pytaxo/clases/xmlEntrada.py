from archivos import nombres,xmlSalida
import alternativa, itertools, operator
from archivos.xmlSalida import despejaAlternativas

class xmlEntrada:
    #atributos estaticos
    
    #atributos de la clase
#     def __init__(self,nombrePregunta,tipo,puntaje,termino,definicion,alternativas):
    def __init__(self,nombre,tipo,puntaje,alternativas,**kwargs):
        #Atributos en comun
        self.nombre=nombre
        self.tipo=tipo
        self.puntaje=puntaje
        self.alternativas=alternativas
        #Atributos solo de preguntas tipo Definicion
        if self.tipo=="definicion":
            self.termino=kwargs['termino']
            #Lista de alternativas de la forma [distractor,{'ponderacion':ponderacion}]
        if self.tipo=="enunciadoIncompleto":
            #Lista donde cada elemento es parte del enunciado ordenado de forma
            #secuencial
            self.enunciadoIncompleto=kwargs['enunciadoIncompleto']
            #Lista donde cada elemento son las respuestas del enunciado
            #ordenadas de forma secuencial
            self.respuestas=kwargs['respuestas']
    
    def printContenidoEntrada(self):
        mensaje="Nombre entrada: {nombre} \nPuntaje: {puntaje}\nTermino: {termino}\nDefinicion: {definicion}\nDistractores: {alternativas} "
        print mensaje.format(nombre=self.nombre,puntaje=self.puntaje, termino=self.termino, definicion=self.definicion,alternativas=self.alternativas)
        pass
    
    #No se sabe si es necesario crear este tipo pues es para un tipo especifico de pregunta
    def preguntaDefSimpleIntoXml(self):
        nombreDirectorioEntradas='./Plantillas'
        if nombres.validaExistenciaArchivo(nombreDirectorioEntradas)==True and nombres.validaCantidadContenido(nombreDirectorioEntradas)==True:
            print nombres.especificDirectoryNames(nombreDirectorioEntradas)
            #falta recoger la informacion y formar la pregunta a partir de la plantilla
        pass
    
    def retornaEnunciadoIncompleto(self):
        return " ".join(self.enunciadoIncompleto)
        
    def retornaAlternativas(self):
        ponderacion={'ponderacion':self.puntaje}
        alternativaCorrecta=list()
        if self.tipo=="definicion":
            alternativaCorrecta.append(self.definicion)
        if self.tipo=="enunciadoIncompleto":
            alternativaCorrecta.append('-'.join(self.respuestas))
        alternativaCorrecta.append(ponderacion)
        alternativas=list()
        alternativas.append(alternativaCorrecta)
        for elem in self.alternativas:
            alternativas.append(elem)
        return alternativas
    #falta reordenar las alternativas pues en este caso siempre la correcta sera la primera
    
    def agrupamientoAlternativas(self):
        listadeListadeAlternativas=list()
        for llave in self.alternativas.keys():
            listadeListadeAlternativas.append(self.alternativas[llave])
        listadeListadeAlternativas=list(itertools.product(*listadeListadeAlternativas))
        for conjuntoAlternativas in listadeListadeAlternativas:
            if xmlSalida.despejaAlternativas(conjuntoAlternativas)==False:
                del conjuntoAlternativas
        return listadeListadeAlternativas

    def agrupamientoAlternativas2(self,cantidadAlternativas):
        listaDeListadeAlternativas=list()
        listaDeAlternativasValidas=list()
        conjuntoPosiblesAlternativas2=list()
        for llave in self.alternativas.keys():
            listaDeListadeAlternativas.append(self.alternativas[llave])
        listadeListadeAlternativas=list(itertools.combinations(listaDeListadeAlternativas,cantidadAlternativas))
        for conjuntoPosiblesAlternativas in listadeListadeAlternativas:
            for conjuntoAlternativas in map(list, conjuntoPosiblesAlternativas2):
                if xmlSalida.validaConjuntoAlternativas(conjuntoAlternativas)==False:
                    #del conjuntoAlternativas
                    conjuntoPosiblesAlternativas2.remove(conjuntoAlternativas)
        #for conjuntoPosiblesAlternativas in listadeListadeAlternativas:
            listaDeAlternativasValidas+=list(itertools.product(*conjuntoPosiblesAlternativas))
        listaDeAlternativasValidas = map(list, listaDeAlternativasValidas)
        print len(listaDeAlternativasValidas)
        for conjuntoAlternativas in listaDeAlternativasValidas[:]:
            if xmlSalida.despejaAlternativas(conjuntoAlternativas)==False:
                listaDeAlternativasValidas.remove(conjuntoAlternativas)
            else:
                pass
               #Se ordenan las alternativas por largo
               #conjuntoAlternativas.sort(key = operator.attrgetter('glosa'))
               #conjuntoAlternativas. (key=lambda x: x.glosa)
        print len(listaDeAlternativasValidas)
        return listaDeAlternativasValidas

    def agrupamientoAlternativas3(self,cantidadAlternativas):
        listaDeListaDeAlternativas=list()
        listaDeAlternativasValidas=list()
        for llave in self.alternativas.keys():
            listaDeListaDeAlternativas.append(self.alternativas[llave])
        for posiblesCombinacionesAlternativas in list(itertools.combinations(listaDeListaDeAlternativas,cantidadAlternativas)):
            for posiblesConjuntos in list(itertools.product(*posiblesCombinacionesAlternativas)):
                if xmlSalida.validaConjuntoAlternativas(posiblesConjuntos)==True:
                        listaDeAlternativasValidas.append(posiblesConjuntos)
        return listaDeAlternativasValidas