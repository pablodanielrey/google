from sqlalchemy import or_
from sqlalchemy.orm import joinedload

from . import Session
from .entities import *

class UsersModel:

    @staticmethod
    def _aplicar_filtros_comunes(q, offset, limit):
        q = q.offset(offset) if offset else q
        q = q.limit(limit) if limit else q
        return q

    @classmethod
    def usuarios(cls, usuario=None, dni=None, c=False, offset=None, limit=None):
        session = Session()
        q = session.query(Usuario)

        q = q.filter(Usuario.id == usuario) if usuario else q
        q = q.filter(Usuario.dni == dni) if dni else q

        q = q.options(joinedload('mails'), joinedload('telefonos'))
        q = q.options(joinedload('claves')) if c else q

        q = cls._aplicar_filtros_comunes(q, offset, limit)
        return q.all()
