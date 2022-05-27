from datetime import datetime

class PostDto:
    def __init__(self, titulo, autor, usuario, imagen, resumen):
        self._titulo = titulo
        self._autor = autor
        self._usuario = usuario
        self._imagen = imagen
        self._resumen = resumen
        self._hora = datetime.now()
        

    @property
    def titulo(self):
        return self._titulo
    
    @titulo.setter
    def titulo(self, valor):
        self._titulo = valor
    
    @property
    def autor(self):
        return self._autor
    
    @autor.setter
    def autor(self, valor):
        self._autor = valor
    
    @property
    def usuario(self):
        return self._usuario
    
    @property
    def imagen(self):
        return self._imagen
    
    @imagen.setter
    def imagen(self, valor):
        self._imagen = valor
    
    @property
    def resumen(self):
        return self._resumen
    
    @resumen.setter
    def resumen(self, valor):
        self._resumen = valor
    
    @property
    def hora(self):
        return self._hora
    
    def __str__(self):
        dia = self.hora.day
        mes = self.hora.month
        anno = self.hora.year
        hora = self.hora.hour
        minuto = self.hora.minute
        return f"Publicado el {dia:02d}/{mes:02d}/{anno:04d} a las {hora:02d}:{minuto:02d} por {self.usuario}"
        
    
    @staticmethod
    def busca(srp, txt_libro: str):
        return srp.find_first(PostDto, lambda l: l.titulo == txt_libro)
    
    # @staticmethod
    # def busca(srp, txt_autor: str):
    #     return srp.filter(PostDto, lambda l: l.autor == txt_autor)
    