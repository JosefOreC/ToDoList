"""
    Clase que se ocupa de la creación de una tarea y su subida a la base de datos.

"""

from src.modelo.entities.tarea import Tarea
from src.modelo.service.session_service.session_manager import SessionManager
from src.modelo.service.task_service.task_service_data import TaskServiceData

from src.modelo.entities.modelo import UsuarioTarea, Usuario, Rol
from src.modelo.service.group_service.group_service_data import GroupServiceData

class RegisterTask:

    def __init__(self, tarea: Tarea, id_grupo: int = None, miembro_disponible: list[list[int, bool]] = None):
        self.tarea = tarea
        self.id_grupo = id_grupo
        if id_grupo:
            if  miembro_disponible== 'all':
                miembros = GroupServiceData.get_all_members_without_master(id_grupo)
                self.users_grupo = [[miembro, True] for miembro in miembros]
            else:
                self.users_grupo = miembro_disponible

        self.relaciones = []

    def __register_task_group(self):
        for miembro, disponible in self.users_grupo:
            self.__register_task_user(miembro, disponible)

    def __register_task_user(self, id_user, disponible: bool = True):
        usuario_tarea = UsuarioTarea(IDUsuario=id_user, IDGrupo=self.id_grupo, Disponible=disponible)
        self.relaciones.append(usuario_tarea)

    def register_task(self):
        if self.id_grupo:
            self.__register_task_group()
        self.__register_task_user(SessionManager.get_instance().usuario.IDUsuario)
        return self.__save_in_db()

    def __save_in_db(self):
        try:
            TaskServiceData.insert_task_user(tarea=self.tarea, usuario_tarea=self.relaciones)
            return True, 'La tarea se agregó con exito'
        except Exception as E:
            return False, E
