

class alternativa:
    
    def __init__(self, llave, tipo, puntaje,glosa, **kwargs):
        self.llave=llave
        self.tipo=tipo
        self.puntaje=puntaje
        self.glosa=glosa
        self.comentario=kwargs['comentario']
    
    def imprimeAlternativa(self):
        return str(self.llave)+' '+str(self.tipo)+' '+str(self.puntaje)+' ' +str(self.glosa)