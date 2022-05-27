from werkzeug import security as safe
from datetime import datetime
import flask_login

class UserDto(flask_login.UserMixin):
        
    def __init__(self, usuario, password, email):
        self._usuario = usuario
        self._email = email
        self._password = safe.generate_password_hash(password)
        self._nombre = ""
        self._descripcion = ""
        self._foto = ""
        
    @property
    def usuario(self):
        return self._usuario
    
    def get_id(self):
        return self._usuario
    
    @property
    def email(self):
        return self._email
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor
    
    @property
    def descripcion(self):
        return self._descripcion
    
    @descripcion.setter
    def descripcion(self, valor):
        self._descripcion = valor
    
    @property
    def foto(self):
        return self._foto
    
    @foto.setter
    def foto(self, valor):
        self._foto = valor
    
    # Comprobar si la contraseña que me pasan es la misma que la
    # del usuario
    def chk_password(self, pswd):
        return safe.check_password_hash(self._password, pswd)
    
    @staticmethod
    def current_user():
        usr = flask_login.current_user
        
        if usr.is_anonymous:
            flask_login.logout_user()
            usr = None
            
        return usr
    
    
    @staticmethod
    def busca(srp, txt_user: str):
        return srp.find_first(UserDto, lambda u: u.usuario == txt_user)
    