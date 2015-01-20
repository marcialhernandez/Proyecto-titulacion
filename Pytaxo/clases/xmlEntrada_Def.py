class xmlEntrada_Def:
    #atributos estaticos
    
    #atributos de la clase
    def __init__(self,nombrePregunta,puntaje,termino,definicion,distractores):
        self.nombre=nombrePregunta
        self.puntaje=puntaje
        self.termino=termino
        self.definicion=definicion
        #Lista de distractores de la forma [distractor,puntaje]
        self.distractores=distractores
    
    def printContenidoEntrada(self):
        mensaje="Nombre entrada: {nombre} \nPuntaje: {puntaje}\nTermino: {termino}\nDefinicion: {definicion}\nDistractores: {distractores} "
        print mensaje.format(nombre=self.nombre,puntaje=self.puntaje, termino=self.termino, definicion=self.definicion,distractores=self.distractores)
        pass