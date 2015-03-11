from archivos import nombres
import alternativa

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