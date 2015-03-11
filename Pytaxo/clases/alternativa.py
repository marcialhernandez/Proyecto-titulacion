

class alternativa:
    
    def __init__(self, llave, tipo, puntaje,glosa, **kwargs):
        self.llave=llave
        self.tipo=tipo
        self.puntaje=puntaje
        self.glosa=glosa
        self.comentario=kwargs['comentario']