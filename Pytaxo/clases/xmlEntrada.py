from archivos import nombres
import itertools, hashlib, copy

class xmlEntrada:
    #atributos estaticos
    
    #atributos de la clase
#     def __init__(self,nombrePregunta,tipo,puntaje,termino,definicion,alternativas):
    def __init__(self,nombre,tipo,puntaje,alternativas,cantidadAlternativas,**kwargs):
        #Atributos en comun
        self.nombre=nombre
        self.tipo=tipo
        self.puntaje=puntaje
        self.alternativas=alternativas
        self.cantidadAlternativas=cantidadAlternativas
        self.id="NULL"
        #Atributos solo de preguntas tipo Definicion
        if self.tipo=="definicion":
            self.termino=kwargs['termino']
            self.id=hashlib.sha256(self.termino).hexdigest()
            #Lista de alternativas de la forma [distractor,{'ponderacion':ponderacion}]
        if self.tipo=="enunciadoIncompleto":
            #Lista donde cada elemento es parte del enunciado ordenado de forma
            #secuencial
            self.enunciado=kwargs['enunciado']
            self.id=hashlib.sha256(self.enunciado).hexdigest()
            #self.id=hashlib.sha256(self.enunciadoIncompleto).hexdigest()
            #Lista donde cada elemento son las respuestas del enunciado
            #ordenadas de forma secuencial
            #self.respuestas=kwargs['respuestas']
    
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
    
    def agrupamientoAlternativas(self,cantidadAlternativas):
        if cantidadAlternativas<=1:
            return list()
        listaDeListaDeAlternativas=list()
        listaDeAlternativasValidas=list()
        for llave in self.alternativas.keys():
            listaDeListaDeAlternativas.append(self.alternativas[llave])
        for posiblesCombinacionesAlternativas in list(itertools.combinations(listaDeListaDeAlternativas,cantidadAlternativas)):
            banderaPresentaACorrecta=False
            for alternativas in posiblesCombinacionesAlternativas:
                if alternativas[0].tipo=='solucion':
                    banderaPresentaACorrecta=True
            if banderaPresentaACorrecta==True:                          
                for posiblesConjuntos in list(itertools.product(*posiblesCombinacionesAlternativas)):
                    listaDeAlternativasValidas.append(posiblesConjuntos)
        #print len(listaDeAlternativasValidas)
        return listaDeAlternativasValidas
    
    def agrupamientoAlternativas2(self,cantidadAlternativas):
        if cantidadAlternativas<=1:
            return list()
        listaDeListaDeAlternativas=list()
        listaDeSoluciones=None
        listaDeAlternativasValidas=list()
        for llave in self.alternativas.keys():
            if self.alternativas[llave][0].tipo=='solucion':
                listaDeSoluciones=self.alternativas[llave]
            else:
                listaDeListaDeAlternativas.append(self.alternativas[llave])      
        for posiblesCombinacionesAlternativas in list(itertools.combinations(listaDeListaDeAlternativas,cantidadAlternativas-1)): 
            posiblesCombinacionesAlternativas=list(posiblesCombinacionesAlternativas)
            posiblesCombinacionesAlternativas.append(listaDeSoluciones)
            for posiblesConjuntos in list(itertools.product(*posiblesCombinacionesAlternativas)):
                listaDeAlternativasValidas.append(posiblesConjuntos)
        #print len(listaDeAlternativasValidas)
        return listaDeAlternativasValidas
    
    def barajaDefiniciones(self):
        return list(itertools.permutations(self.alternativas['terminos'].keys()))
    
    def agrupamientoPareado(self, cantidadAlternativas):
        if cantidadAlternativas<=1:
            return list()
        listaConjuntoTerminos=list(itertools.permutations(self.alternativas['terminos'].keys()))
#         for conjuntoTerminos in list(itertools.permutations(self.alternativas['terminos'].keys())):
#             listaConjuntoTerminos.append(conjuntoTerminos)
        #para cada variante de termino pareado
        for conjuntoTerminos in listaConjuntoTerminos:
            listaDeListaDeOpciones=list()
            conjuntoSoluciones=None
            distractores=list()
            #Es solucion pero esta desordenada
            pozoDistractoresPordesorden=None
            #No es solucion pues uno de sus terminos es en realidad un distractor
            pozoDistractoresPorDistractor=list()
            #No es solucion pues 2 de sus terminos son distractores
            pozoDistractoresPorDistractorDoble=list()
            banderaDobleDistractor=False
            if len(self.alternativas['distractores'].keys())>1:
                banderaDobleDistractor=True #Como existen mas de 2 tipos de distractores           
            for cadaDefinicion in conjuntoTerminos:
                posiblesTerminos=list()
                for cadaTermino in self.alternativas['terminos'][cadaDefinicion]:
                    posiblesTerminos.append(cadaTermino)
                listaDeListaDeOpciones.append(posiblesTerminos)
                if cadaDefinicion in self.alternativas['distractores'].keys():
                    #Con esto se evita errores de intentar acceder a una llave que no existe
                    for cadaDistractor in self.alternativas['distractores'][cadaDefinicion]:
                        distractores.append(cadaDistractor)
            #Se obtiene una lista de posibles soluciones de la variante actual
            conjuntoSoluciones=list(itertools.product(*listaDeListaDeOpciones))
            #Para cada solucion de la variante actual
            for solucion in conjuntoSoluciones:
                #Se obtiene el primer pozo de distractores, derivado de las posibles ordenamientos
                #de la solucion###########
                #pozoDistractoresPordesorden=list(itertools.permutations(solucion))
                #pozoDistractoresPordesorden.remove(solucion)###########
                #El segundo pozo de distractores consiste en reemplazar 1 elemento
                #de la solucion por 1 de la lista de distractores
                #el reemplazo tiene que se por ID, significa que se reemplaza
                #un termino por su propio distractor
                dobleDistractorPendientes=list()
                if len(distractores)>=1:
                    #En caso que no hayan distractores, no se realizara este proceso
                    for cadaDistractor in distractores:
                        contador=0
                        for cadaTermino in solucion:
                            if cadaTermino.llave==cadaDistractor.llave:
                                conjuntoDistractor=list(solucion)
                                conjuntoDistractor[contador]=cadaDistractor
                                if conjuntoDistractor not in pozoDistractoresPorDistractor:
                                    pozoDistractoresPorDistractor.append(conjuntoDistractor)
                                dobleDistractorPendientes.append(copy.copy(conjuntoDistractor))
                                break
                            contador+=1
                        #En caso que no hayan mas de un tipo de distractor, no se realizara este proceso
                        if len(dobleDistractorPendientes)>0 and banderaDobleDistractor==True:
                            i=0
                            for elem in dobleDistractorPendientes[0]:
                                if elem.llave==cadaDistractor.llave and elem.tipo=='solucion':
                                    conjuntoDistractorDoble=list(dobleDistractorPendientes[0])
                                    conjuntoDistractorDoble[i]=cadaDistractor
                                    if conjuntoDistractorDoble not in pozoDistractoresPorDistractorDoble:
                                        pozoDistractoresPorDistractorDoble.append(conjuntoDistractorDoble)
                                    dobleDistractorPendientes.remove(dobleDistractorPendientes[0])
                                    break
                                i+=1
            print dobleDistractorPendientes[0][0].imprimeAlternativa()
#             while len(dobleDistractorPendientes)>0:
#                 for cadaDistractor in distractores:
#                     i=0
#                     for elem in dobleDistractorPendientes[0]:
#                                 if elem.llave==cadaDistractor.llave and elem.tipo=='solucion':
#                                     conjuntoDistractorDoble=list(dobleDistractorPendientes[0])
#                                     print len(conjuntoDistractorDoble)
#                                     #conjuntoDistractorDoble[i]=cadaDistractor
#                                     if conjuntoDistractorDoble not in pozoDistractoresPorDistractorDoble:
#                                         pozoDistractoresPorDistractorDoble.append(conjuntoDistractorDoble)
#                                     dobleDistractorPendientes.remove(dobleDistractorPendientes[0])
#                                     break
#                                 i+=1
            print '!!!'                             
            for conjunto in  pozoDistractoresPorDistractorDoble:
                print '@'
                for lala in conjunto:
                    print lala.imprimeAlternativa()
            pass
    