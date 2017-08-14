from sqlalchemy import or_, func
from sqlalchemy.orm import joinedload
from google.model.GoogleAuthApi import GAuthApis

import os
import requests
from dateutil.parser import parse
import datetime
import hashlib
from apiclient import errors


from . import Session
from .entities import *

class GoogleModel:

    usuarios_url = os.environ['USERS_REST_URL']

    @staticmethod
    def _aplicar_filtros_comunes(q, offset, limit):
        q = q.offset(offset) if offset else q
        q = q.limit(limit) if limit else q
        return q


    @classmethod
    def actualizarUsuarios(cls, uid=None):
        usuarios = []
        session = Session()
        try:
            if uid:
                usuarios.append(requests.get(cls.usuarios_url + '/usuarios/'+ uid +'?c=True').json())
            else:
                result = session.query(func.max(Sincronizacion.actualizado)).first()
                result = result if result[0] else  session.query(func.max(Sincronizacion.creado)).first()
                fecha = result[0]
                filter = '/usuarios/?c=True'
                if fecha:
                    # filter = filter + '&f=' + str(fecha) descomentar cuando se pase a produccion
                    filter = filter + '&f=2017-08-02%2008:08:46.573983' #comentar cuando se pase a produccion
                usuarios = requests.get(cls.usuarios_url + filter + '&limit=10').json() #comentar cuando se pase a produccion
                # usuarios = requests.get(cls.usuarios_url + filter).json() descomentar cuando se pase a produccion

            for u in usuarios:
                emails = [m['email'] for m in u['mails'] if 'econo.unlp.edu.ar' in m['email']]
                print(emails)
                continue
                r = session.query(Sincronizacion).filter(Sincronizacion.id == u['id']).first()
                clave = u['claves'][0] if len(u['claves']) > 0 else None
                if clave is None:
                    continue

                if r[0]:
                    # actualizar
                    print('update' + r[0])
                else:
                    # crear usuario
                    s = Sincronizacion(
                        id=u['id'],
                        dni=u['dni'],
                        clave_id=clave['id'],
                        clave=clave['clave'],
                        clave_actualizada = parse(clave['actualizado']) if clave['actualizado'] and clave['actualizado'] != 'null' else parse(clave['creado'])
                    )
                    session.add(s)

                '''
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
                '''
                session.commit()

            return usuarios
        finally:
            session.close()

    @classmethod
    def sincronizarClave(cls):
        session = Session()
        try:
            q = session.query(Sincronizacion).filter(or_(Sincronizacion.sincronizado == None, Sincronizacion.sincronizado < Sincronizacion.clave_actualizada))

            sync = []
            noSync = []
            service = GAuthApis.getService()
            fecha = datetime.datetime.now()
            for s in q:
                userGoogle = s.dni + '@econo.unlp.edu.ar'
                try:
                    #update user
                    r = service.users().update(userKey=userGoogle,body={"password":s.clave}).execute()
                    qq = session.query(Sincronizacion).filter(Sincronizacion.id == s.id)
                    ss = qq.all()[0]
                    ss.sincronizado = fecha
                    session.commit()
                    sync.append(s.dni)

                except errors.HttpError as err:
                    print("el usuario no existe")
                    noSync.append(s.dni)

            return {'sincronizados':sync, 'noSincronizados':noSync}
        finally:
            session.close()


        @classmethod
        def sincronizarClave(cls,id):
            cls.sincronizarUsuarios(id)
            cls.sincronizar()
            return



        return {status:'OK'}
