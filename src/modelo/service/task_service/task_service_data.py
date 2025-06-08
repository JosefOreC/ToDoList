"""
Clase que controla la entidad tarea y relacionados
desde la base de datos CRUD.
"""


from src.modelo.database_management.base.declarative_base import session
from src.modelo.entities.modelo import UsuarioTarea, Tarea, Grupo
from src.modelo.service.session_service.session_manager import SessionManager
from src.modelo.service.data_service.data_format import DataFormat
from datetime import date
from src.modelo.service.task_service.update_task import UpdateTask

class TaskServiceData:
    @staticmethod
    def insert_task_user(tarea: Tarea, usuario_tarea: list[UsuarioTarea]):
        """
        Inserta una tarea y sus relaciones con usuarios en la base de datos.

        Args:
            tarea (Tarea): Instancia de la tarea a guardar.
            usuario_tarea (list[UsuarioTarea]): Lista de relaciones usuario-tarea.
        """
        session.add_all([tarea])
        session.flush()
        for relacion in usuario_tarea:
            relacion.IDTarea = tarea.IDTarea
        session.add_all(usuario_tarea)
        session.commit()

    @staticmethod
    def update_task_user(id_usuario, id_tarea, nombre = None,
                         fecha = None, prioridad = None, disponible = None,
                         realizado = None, detalle = None, archivado = None):

        """
        Actualiza los datos de una tarea relacionada a un usuario específico.

        Args:
            id_usuario (int): ID del usuario.
            id_tarea (int): ID de la tarea.
            nombre (str): Nuevo nombre de la tarea.
            fecha (date): Nueva fecha programada.
            prioridad (int, optional): Nueva prioridad.
            disponible (bool, optional): Estado de disponibilidad.
            realizado (bool, optional): Estado de realización.
            detalle (str, optional): Nuevo detalle de la tarea.
            archivado (bool, optional): Estado de archivado.
        """
        updatedata = UpdateTask(id_tarea, id_usuario)

        if nombre:
            updatedata.update_name(nombre)
        if archivado is not None:
            updatedata.update_archivado(archivado)
        if fecha:
            updatedata.update_fecha(fecha)
        if prioridad:
            updatedata.update_prioridad(prioridad)
        if disponible is not None:
            updatedata.update_disponible(disponible)
        if realizado is not None:
            updatedata.update_realizado(realizado)
        if detalle:
            updatedata.update_detalle(detalle)

        session.commit()


    @staticmethod
    def get_tasks_user_list_date(usuario_id: int, fecha_inicio: str or date, fecha_fin: str or date = None,
                                 activo = True,
                                 archivado = False):
        fecha_inicio = DataFormat.convertir_fecha(fecha_inicio)
        if not fecha_fin:
            fecha_fin = fecha_inicio
        else:
            fecha_fin = DataFormat.convertir_fecha(fecha_fin)

        if fecha_fin < fecha_inicio:
            raise Exception(f'La fecha de inicio {fecha_inicio} es mayor a la fecha de fin {fecha_fin}. '
                            f'\nNo se recuperó datos.')
        resultados = session.query(Tarea,
                                   UsuarioTarea.Disponible,
                                   UsuarioTarea.Realizado, UsuarioTarea.IDGrupo).join(UsuarioTarea,
                                   UsuarioTarea.IDUsuario==usuario_id).filter(UsuarioTarea.IDTarea==Tarea.IDTarea,
                                   Tarea.Fecha_programada >= fecha_inicio,
                                   Tarea.Fecha_programada <= fecha_fin,
                                   Tarea.Activo == activo,
                                   UsuarioTarea.Archivado == archivado).order_by(Tarea.Prioridad.asc()).all()
        return resultados

    @staticmethod
    def __get_all_task():
        return session.query(Tarea.Nombre, Tarea.Fecha_programada, Tarea.Detalle, Tarea.Prioridad, Tarea.Activo)

    @staticmethod
    def get_tasks_user_list_all(usuario_id: int, activo=True, archivado=False):

        resultados = session.query(Tarea,
                                    UsuarioTarea.Disponible,
                                    UsuarioTarea.Realizado, UsuarioTarea.IDGrupo).join(UsuarioTarea,
                                    UsuarioTarea.IDUsuario == usuario_id).filter(
                                    UsuarioTarea.IDTarea == Tarea.IDTarea,
                                    Tarea.Activo == activo,
                                    UsuarioTarea.Archivado == archivado).order_by(Tarea.Prioridad.asc()).all()
        return resultados

    @staticmethod
    def get_task_user_archivade(usuario_id: int):
        return TaskServiceData.get_tasks_user_list_all(usuario_id, archivado = False)

    @staticmethod
    def get_tasks_session_user_list_date(fecha: str or date):
        usuario_id = SessionManager.get_instance().usuario.IDUsuario
        return TaskServiceData.get_tasks_user_list_date(usuario_id, fecha)

    @staticmethod
    def get_tasks_session_user_list_today():
        return TaskServiceData.get_tasks_session_user_list_date(date.today())
    
    @staticmethod
    def get_task(id_tarea):
        return session.query(Tarea).filter_by(IDTarea=id_tarea).first().all()
            
    @staticmethod
    def soft_delete_task(id_tarea):
        actualizacion = UpdateTask(id_tarea)
        actualizacion.update_activo(False)
        session.commit()

    @staticmethod
    def get_relations_of_task(id_tarea):
        return session.query(UsuarioTarea).filter_by(IDTarea=id_tarea).all()

    @staticmethod
    def get_id_group_of_task(id_tarea):
        response = session.query(UsuarioTarea.IDGrupo).filter_by(IDTarea=id_tarea).first()[0]
        return response if response else None

    @staticmethod
    def is_editable_task_for_user(id_tarea, id_usuario):
        """
            Parametros: Id de la tarea e Id del usuario
            Retorna si una tarea es editable para un usuario.
        """
        return session.query(UsuarioTarea.Disponible).filter_by(IDTarea=id_tarea, IDUsuario=id_usuario).first()[0]

    @staticmethod
    def __delete_task(id_tarea):

        relaciones = TaskServiceData.get_relations_of_task(id_tarea)
        tarea = TaskServiceData.get_task(id_tarea)
        for relacion in relaciones:
            session.delete(relacion)

        session.delete(tarea)
        session.commit()







