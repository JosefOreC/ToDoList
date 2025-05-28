"""

"""

from src.modelo.entities.tarea import Tarea
from src.modelo.service.session_service.session_manager import SessionManager
from src.modelo.service.task_service.task_service_data import TaskServiceData
from src.modelo.entities.usuario import Usuario
from src.modelo.entities.usuario_tarea import UsuarioTarea

class RegisterTask:
    def __init__(self, tarea: Tarea, id_grupo: str = None, users_grupo_disponible: list[[Usuario.IDUsuario, bool]] = None):
        self.tarea = tarea
        self.id_grupo = id_grupo
        #if id_grupo:
        #    if users_grupo_disponile == 'all':
        #        self.users_grupo = [funcion_recuperacion_datos_id_user_grupo]


    def __register_task_group(self):
        pass

    def __register_task_user(self, id_user, id_group = None, disponible: bool = True):
        usuario_tarea = UsuarioTarea(IDUsuario=id_user, IDGrupo=id_group, Disponible=disponible)
        return self.__save_in_db(usuario_tarea)

    def register_task(self):
        if self.id_grupo:
            return self.__register_task_group()
        return self.__register_task_user(SessionManager.get_instance().usuario.IDUsuario)

    def __save_in_db(self, usuario_tarea):
        try:
            TaskServiceData.insert_task_user(tarea=self.tarea, usuario_tarea=usuario_tarea)
            return True, 'La tarea se agregó con exito'
        except Exception as E:
            return False, E
