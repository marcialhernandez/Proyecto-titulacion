from archivos import nombres

class xmlEntrada:
    #atributos estaticos
    
    #atributos de la clase
    def __init__(self,nombrePregunta,puntaje,termino,definicion,distractores):
        self.nombre=nombrePregunta
        self.puntaje=puntaje
        self.termino=termino
        self.definicion=definicion
        #Lista de distractores de la forma [distractor,{'ponderacion':ponderacion}]
        self.distractores=distractores
    
    def printContenidoEntrada(self):
        mensaje="Nombre entrada: {nombre} \nPuntaje: {puntaje}\nTermino: {termino}\nDefinicion: {definicion}\nDistractores: {distractores} "
        print mensaje.format(nombre=self.nombre,puntaje=self.puntaje, termino=self.termino, definicion=self.definicion,distractores=self.distractores)
        pass
    
    #No se sabe si es necesario crear este tipo pues es para un tipo especifico de pregunta
    def preguntaDefSimpleIntoXml(self):
        nombreDirectorioEntradas='./Plantillas'
        if nombres.validaExistenciaArchivo(nombreDirectorioEntradas)==True and nombres.validaCantidadContenido(nombreDirectorioEntradas)==True:
            print nombres.especificDirectoryNames(nombreDirectorioEntradas)
            #falta recoger la informacion y formar la pregunta a partir de la plantilla
        pass
    
    def retornaAlternativas(self):
        ponderacion={'ponderacion':self.puntaje}
        alternativaCorrecta=list()
        alternativaCorrecta.append(self.definicion)
        alternativaCorrecta.append(ponderacion)
        alternativas=list()
        alternativas.append(alternativaCorrecta)
        for elem in self.distractores:
            alternativas.append(elem)
        return alternativas
    #falta reordenar las alternativas pues en este caso siempre la correcta sera la primera