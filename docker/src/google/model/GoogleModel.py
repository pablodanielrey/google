from sqlalchemy import or_
from sqlalchemy.orm import joinedload

import os
import requests
from dateutil.parser import parse
import datetime

from . import Session
from .entities import *

class GoogleModel:

    usuarios_url = os.environ['USERS_REST_URL']

    @staticmethod
    def _aplicar_filtros_comunes(q, offset, limit):
        q = q.offset(offset) if offset else q
        q = q.limit(limit) if limit else q
        return q

    @staticmethod
    def obtenerUsuario(usuario):
        return requests.get(cls.usuarios_url + '/usuarios/{}'.format(usuario)).json()[0]

    @classmethod
    def sincronizarUsuarios(cls):
        usuarios = requests.get(cls.usuarios_url + '/usuarios/?c=True').json()
        session = Session()
        for u in usuarios:
            s = session.query(Sincronizacion).filter(Sincronizacion.id == u['id']).first()
            clave = u['claves'][0] if len(u['claves']) > 0 else None
            if clave:
                if not s:
                    s = Sincronizacion(
                        id=u['id'],
                        dni=u['dni'],
                        clave_id=clave['id'],
                        clave=clave['clave'],
                        clave_actualizada = parse(clave['actualizado']) if clave['actualizado'] and clave['actualizado'] != 'null' else parse(clave['creado'])
                    )
                    session.add(s)
                else:
                    if clave['actualizado'] and clave['actualizado'] != 'null' and parse(clave['actualizado']) > s.clave_actualizada:
                        s.clave = clave['clave'],
                        s.clave_actualizada = parse(clave['actualizado'])
                session.commit()

        return {'estado':'OK'}




    @classmethod
    def sincronizar(cls):
        session = Session()
        q = session.query(Sincronizacion).filter(or_(Sincronizacion.sincronizado == None, Sincronizacion.sincronizado < Sincronizacion.clave_actualizada))
        return q.all()

        """

        session = Session()
        q = session.query(Sincronizacion)
        q = q.order_by(Sincronizacion.sincronizado.desc()).limit(1)

        for s in q:
            s.id
            s.sincronizado

        fecha = datetime.datetime.now()
        '''
            sincronizo a google
            for c in claves:
                sincr ---> google
                if sinc == ok:
                    q = session.query(Sincronizacion).filter(Sincronizacion.id == sinc.id)
                    ss = q.all()[0]
                    ss.sincronizado = fecha
                    ss.save()
        ''''
        """

        return {'estado':'OK'}


        @classmethod
        def sincronizarClave(cls,id):
            cls.sincronizarUsuarios(id)
            cls.sincronizar()
            return



        return {status:'OK'}
