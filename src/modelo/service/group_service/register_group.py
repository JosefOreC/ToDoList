"""


"""

from src.modelo.service.group_service.group_service_data import GroupServiceData
from src.modelo.entities.modelo import Grupo, UsuarioGrupo, Rol
from datetime import datetime

class RegisterGroup:
    def __init__(self, grupo: Grupo, miembros_id: list[int]=None):
        self.grupo = grupo
        self.miembros = miembros_id
        self.__relation_list = []

    def register_group(self):
        self.__relation_list.append(self.__relation_user_master_group())

        if self.miembros:
            for miembro in self.miembros:
                self.__add_member_group(miembro)

        self.__save_group()

    def __relation_user_master_group(self):
        return UsuarioGrupo(IDUsuario=self.grupo.IDMaster, rol = Rol.master)

    def __add_member_group(self, miembro: int):
        self.__relation_list.append(UsuarioGrupo(IDUsuario=miembro, rol=Rol.miembro))

    def __save_group(self):
        GroupServiceData.insert_group(self.grupo, self.__relation_list)

    @staticmethod
    def create_primitive_group(nombre: str, id_master: int, descripcion:str=None) -> Grupo:
        return Grupo(Nombre=nombre, IDMaster = id_master, Descripcion=descripcion, Fecha_creacion = datetime.today())
