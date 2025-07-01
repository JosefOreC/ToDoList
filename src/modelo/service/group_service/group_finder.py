"""
    Encargado de buscar grupos por nombre
"""
from src.modelo.database_management.base.declarative_base import session
from src.modelo.entities.grupo import Grupo
from src.modelo.entities.usuario_grupo import UsuarioGrupo

class GroupFinder:
    @staticmethod
    def search_for_group_by_name(id_usuario:int , nombre:str):
        nombre = nombre.lower()

        return session.query(Grupo).join(UsuarioGrupo, UsuarioGrupo.IDGrupo==Grupo.IDGrupo).filter(
            UsuarioGrupo.IDUsuario == id_usuario, Grupo.Nombre.ilike(f'%{nombre}%')
        ).all()

    @staticmethod
    def search_for_group_by(id_usuario: int, nombre: str=None, rol: str = None):
        filtros = [UsuarioGrupo.IDUsuario==id_usuario]
        if nombre or nombre != '':
            filtros.append(Grupo.Nombre.ilike(f'%{nombre}%'))
        if rol:
            filtros.append(UsuarioGrupo.rol == rol)

        filtros = tuple(filtros)

        return (session.query(Grupo.IDGrupo, Grupo.Nombre, Grupo.Descripcion, UsuarioGrupo.rol).
                join(UsuarioGrupo, UsuarioGrupo.IDGrupo == Grupo.IDGrupo).filter(*filtros).all())
