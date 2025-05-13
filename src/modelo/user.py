"""
    Crea la super clase Usuario
    define los metodos de la actualizacion de datos básicos
    para las subclases Operador e Integrante
"""

class User:
    """
        Super clase usuario
        métodos y atributos basicos para el manejo
        de usuarios de la aplicacion
    """

    _IDUser: str
    alias: str
    name: str
    apellido_paterno: str
    apellido_materno: str

    def __init__(self, initial_id, alias, name= None, apellido_p = None, apellido_m=None):
        self._IDUser = initial_id
        self.alias= alias
        if name:
            self.name = name
        if apellido_p:
            self.apellido_paterno = apellido_p
        if apellido_p:
            self.apellido_materno = apellido_m

    def get_full_name(self):
        return self.name + self.apellido_paterno + self.apellido_materno

    def set_apellido_paterno(self, apellido_paterno):
        self.apellido_paterno = apellido_paterno

    def set_apellido_materno(self, apellido_materno):
        self.apellido_materno = apellido_materno

    def update_id(self, new_id):
        self._IDUser = new_id

    def get_alias(self):
        return self.alias

    def set_alias(self, alias):
        self.alias = alias

if __name__ == "__main__":
    pass