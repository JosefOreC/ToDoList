"""
Clase que se ocupa de la creación de una tarea y su subida a la base de datos.
"""
from src.modelo.database_management.base.declarative_base import session
from src.modelo.entities.tarea import Tarea
from src.modelo.service.session_service.session_manager import SessionManager
from src.modelo.service.task_service.task_service_data import TaskServiceData

from src.modelo.entities.modelo import UsuarioTarea, Usuario, Rol
from src.modelo.service.group_service.group_service_data import GroupServiceData

class RegisterTask:
    """
    Clase encargada del registro de una tarea, ya sea individual o grupal.

    Permite crear una tarea y asociarla con uno o varios usuarios en función
    del grupo al que pertenezcan, además de establecer si están disponibles o no.
    """

    def __init__(self, tarea: Tarea, id_grupo: int = None, miembro_disponible: list[list[int, bool]] = None,
                 anadir=False):
        """
        Inicializa una instancia de RegisterTask.

        Args:
            tarea (Tarea): Objeto de la tarea que se va a registrar.
            id_grupo (int, optional): ID del grupo al que se asociará la tarea.
            miembro_disponible (list[list[int, bool]] or str, optional): Lista de pares [id_usuario, disponible].
                Si se pasa 'all', se asignará la tarea a todos los miembros del grupo como disponibles.
        """
        self.tarea = tarea
        self.id_grupo = id_grupo
        if id_grupo:
            if  miembro_disponible== 'all':
                miembros = GroupServiceData.get_all_members(id_grupo)
                self.users_grupo = [[miembro, True] for miembro in miembros]
                for miem, dispo in self.users_grupo:
                    if miem == SessionManager.get_id_user():
                        ind = self.users_grupo.index([miem, dispo])
                        self.users_grupo[ind] = [None, None]
                        break
            else:
                self.users_grupo = miembro_disponible

        self.anadir = anadir

        self.relaciones = []

    def __register_task_group(self):
        """
        Registra la tarea para todos los miembros del grupo según disponibilidad.
        """
        for miembro, disponible in self.users_grupo:
            if miembro is None and disponible is None:
                us = session.query(UsuarioTarea).filter_by(IDUsuario=SessionManager.get_id_user(),
                                                           IDTarea=self.tarea.IDTarea).first()
                us.IDGrupo = self.id_grupo
                session.commit()
                continue
            self.__register_task_user(miembro, disponible)

    def __register_task_user(self, id_user, disponible: bool = True):
        """
        Crea una relación entre un usuario y la tarea.

        Args:
            id_user (int): ID del usuario a asociar con la tarea.
            disponible (bool): Indica si el usuario tiene disponible la tarea para edición.
        """
        if self.anadir:
            usuario_tarea = UsuarioTarea(IDUsuario=id_user, IDGrupo=self.id_grupo, IDTarea=self.tarea.IDTarea,
                                         Disponible=disponible)
        else:
            usuario_tarea = UsuarioTarea(IDUsuario=id_user, IDGrupo=self.id_grupo, Disponible=disponible)
        self.relaciones.append(usuario_tarea)

    def register_task(self):
        if self.id_grupo:
            self.__register_task_group()
        else:
            self.__register_task_user(SessionManager.get_instance().usuario.IDUsuario)
        return self.__save_in_db()

    def __save_in_db(self):

        if self.anadir:
            session.add_all(self.relaciones)
            session.commit()
            return True, 'La tarea se agregó con éxito'
        try:
            TaskServiceData.insert_task_user(tarea=self.tarea, usuario_tarea=self.relaciones)
            return True, 'La tarea se agregó con exito'
        except Exception as E:
            return False, E
