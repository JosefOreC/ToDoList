"""


"""

from src.modelo.service.group_service.group_service_data import GroupServiceData
from src.modelo.entities.modelo import Grupo, UsuarioGrupo, Rol
from datetime import datetime

class RegisterGroup:
    """
    Clase encargada de registrar un nuevo grupo y establecer relaciones con sus miembros.

    Atributos:
        grupo (Grupo): Objeto Grupo que se desea registrar.
        miembros (list[int], opcional): Lista de IDs de usuarios que serán miembros del grupo.
        __relation_list (list[UsuarioGrupo]): Lista interna de relaciones entre el grupo y los usuarios.
    """

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
        """
        Crea una instancia primitiva de un grupo sin persistirla.

        Args:
            nombre (str): Nombre del grupo.
            id_master (int): ID del usuario que será el master del grupo.
            descripcion (str, opcional): Descripción del grupo.

        Returns:
            Grupo: Objeto Grupo instanciado con los valores proporcionados.
        """
        return Grupo(Nombre=nombre, IDMaster = id_master, Descripcion=descripcion, Fecha_creacion = datetime.today())
