from datetime import datetime

class CommentDto:
    def __init__(self, libro, comentario, usuario, valoracion):
        self._libro = libro
        self._comentario = comentario
        self._usuario = usuario
        self._valoracion = valoracion
        self._hora = datetime.now()
        self._id = f"{self._usuario}{self._hora}"
    
    
    @property
    def id(self):
        return self._id
    
    @property
    def libro(self):
        return self._libro
    
    @property
    def usuario(self):
        return self._usuario
    
    @property
    def comentario(self):
        return self._comentario
    
    @property
    def valoracion(self):
        return self._valoracion

    @property
    def hora(self):
        return self._hora
    
    @property
    def fecha(self):
        dia = self.hora.day
        mes = self.hora.month
        anno = self.hora.year
        hora = self.hora.hour
        minuto = self.hora.minute
        return f"{dia:02d}/{mes:02d}/{anno:04d} a las {hora:02d}:{minuto:02d}"

    def __str__(self):
        dia = self.hora.day
        mes = self.hora.month
        anno = self.hora.year
        hora = self.hora.hour
        minuto = self.hora.minute
        return f"{self.usuario} - {dia:02d}/{mes:02d}/{anno:04d} {hora:02d}:{minuto:02d}\n {self.comentario}"
    
    
    @staticmethod
    def busca(srp, txt_id):
        return srp.find_first(CommentDto, lambda c: c.id == txt_id)
    