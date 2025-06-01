"""


"""
from src.modelo.entities.modelo import Grupo, UsuarioGrupo
from src.modelo.database_management.base.declarative_base import session
from sqlalchemy.exc import IntegrityError

class GroupServiceData:
    @staticmethod
    def insert_group(grupo: Grupo,relation_list: list[UsuarioGrupo]):
        try:
            session.add_all([grupo])
            session.flush()
            for miembro in relation_list:
                miembro.IDGrupo = grupo.IDGrupo
            session.add_all(relation_list)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise Exception('Ya existe un grupo con el mismo nombre.')