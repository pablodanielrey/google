from sqlalchemy import or_, func, and_
from sqlalchemy.orm import joinedload
from google.model.GoogleAuthApi import GAuthApis

import os
import uuid
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
                usuarios = requests.get(cls.usuarios_url + filter + '&limit=50').json() #comentar cuando se pase a produccion
                # usuarios = requests.get(cls.usuarios_url + filter).json() descomentar cuando se pase a produccion

            actualizados = 0
            creados = 0
            for u in usuarios:
                emails = [m['email'] for m in u['mails'] if 'econo.unlp.edu.ar' in m['email'] and m['confirmado']]
                sinc = session.query(Sincronizacion).filter(Sincronizacion.id == u['id']).first()

                clave = u['claves'][0] if len(u['claves']) > 0 else None
                if clave is None or len(emails) <= 0:
                    print("No tiene correos o clave")
                    continue

                emails = ",".join([x for x in sorted(emails)])
                clave_actualizada = parse(clave['actualizado']) if clave['actualizado'] and clave['actualizado'] != 'null' else parse(clave['creado'])

                if sinc:
                    ''' actualizo los datos que fueron modificados '''
                    modificado = False
                    if sinc.clave != clave['clave']:
                        sinc.clave = clave['clave']
                        sinc.clave_actualizada = clave_actualizada
                        sinc.clave_id = clave['id']
                        modificado = True

                    if emails != sinc.emails:
                        sinc.emails = emails
                        modificado = True

                    actualizados = actualizados + 1 if modificado else actualizados

                else:
                    ''' crear usuario '''
                    s = Sincronizacion(
                        id=u['id'],
                        dni=u['dni'],
                        clave_id=clave['id'],
                        clave=clave['clave'],
                        clave_actualizada=parse(clave['actualizado']) if clave['actualizado'] and clave['actualizado'] != 'null' else parse(clave['creado']),
                        emails=emails
                    )
                    session.add(s)
                    creados = creados + 1

                session.commit()

            return {'actualizados':actualizados, 'creados':creados}
        finally:
            session.close()

    @classmethod
    def sincronizarClaves(cls):
        session = Session()
        try:
            q = session.query(Sincronizacion).filter(or_(Sincronizacion.clave_sincronizada == None, Sincronizacion.clave_sincronizada < Sincronizacion.clave_actualizada))

            sync = []
            noSync = []
            service = GAuthApis.getServiceAdmin()
            fecha = datetime.datetime.now()
            for s in q:
                userGoogle = s.dni + '@econo.unlp.edu.ar'
                try:
                    #update user
                    r = service.users().update(userKey=userGoogle,body={"password":s.clave}).execute()
                    qq = session.query(Sincronizacion).filter(Sincronizacion.id == s.id)
                    ss = qq.all()[0]
                    ss.clave_sincronizada = fecha

                    ds = cls._crearLog(r)
                    session.add(ds)

                    session.commit()
                    sync.append(s.dni)

                except errors.HttpError as err:
                    print("el usuario no existe")
                    noSync.append(s.dni)

            return {'sincronizados':sync, 'noSincronizados':noSync}
        finally:
            session.close()

    @classmethod
    def _crearLog(cls, r):
        return DatosDeSincronizacion(
                    id= str(uuid.uuid4()),
                    fecha_sincronizacion=datetime.datetime.now(),
                    respuesta=str(r)
                )

    @classmethod
    def sincronizarUsuarios(cls):
        session = Session()
        try:
            q = session.query(Sincronizacion).filter(or_(Sincronizacion.usuario_creado == None,
                and_(Sincronizacion.usuario_actualizado == None, Sincronizacion.actualizado > Sincronizacion.usuario_creado),
                Sincronizacion.actualizado > Sincronizacion.usuario_actualizado
                ))

            creados = []
            actualizados = []
            service = GAuthApis.getServiceAdmin()
            fecha = datetime.datetime.now()

            for s in q:
                userGoogle = s.dni + '@econo.unlp.edu.ar'
                user = requests.get(cls.usuarios_url + '/usuarios/'+ s.id +'?c=True').json()
                fullName = user["nombre"] + " " + user["apellido"]

                cls.agregarAliasEnviarComo(fullName, 'pruebaparagoogle@econo.unlp.edu.ar', userGoogle)
                return
                try:
                    # datos a actualizar
                    datos = {}

                    datos["name"] = {"familiyName": user["nombre"], "givenName": user["apellido"], "fullName": fullName}

                    r = service.users().update(userKey=userGoogle,body=datos).execute()
                    ds = cls._crearLog(r)
                    session.add(ds)

                    # actualizar alias
                    r = service.users().aliases().list(userKey=userGoogle).execute()
                    aliases = [a['alias'] for a in r.get('aliases', [])]
                    for e in s.emails.split(","):
                        if e not in aliases:
                            r = service.users().aliases().insert(userKey=userGoogle,body={"alias":e}).execute()
                            ds = cls._crearLog(r)
                            session.add(ds)

                    s.usuario_actualizado = fecha

                    session.commit()

                    actualizados.append(datos)
                except errors.HttpError as err:
                    # crear usuario
                    datos = {}
                    datos["aliases"] = s.emails.split(",")
                    datos["changePasswordAtNextLogin"] = False
                    datos["primaryEmail"] = userGoogle
                    datos["emails"] = [{'address': userGoogle, 'primary': True, 'type': 'work'}]

                    datos["name"] = {"givenName": user["nombre"], "fullName": fullName, "familyName": user["apellido"]}
                    datos["password"] = s.clave
                    datos["externalIds"] = [{'type': 'custom', 'value': s.id}]


                    r = service.users().insert(body=datos).execute()


                    ds = cls._crearLog(r)
                    session.add(ds)

                    # crear alias
                    for e in s.emails.split(","):
                        print("Correo a agregar enviar como:{}".format(e))
                        r = service.users().aliases().insert(userKey=userGoogle,body={"alias":e}).execute()
                        ds = cls._crearLog(r)
                        session.add(ds)

                        cls.agregarAliasEnviarComo(fullName, e, userGoogle)

                    s.usuario_creado = fecha
                    s.usuario_actualizado = fecha

                    session.commit()

                    creados.append(datos)

            return {'creados':creados, 'actualizados':actualizados}
        finally:
            session.close()


    @classmethod
    def agregarAliasEnviarComo(cls, name, email, userKeyG):
        alias = {
            'displayName': name,
            'replyToAddress': email,
            'sendAsEmail': email,
            'treatAsAlias': True,
            'isPrimary': False,
            'isDefault': True
        }
        print("enviar como:{}".format(name))
        print("alias:{}".format(alias))
        session = Session()
        try:

            try:
                # gmail = GAuthApis.getServiceGmail(userKeyG)
                gmail = GAuthApis.getServiceGmail()
                
                r = gmail.users().settings().sendAs().list(userId='me').execute()
                aliases = [ a['sendAsEmail'] for a in r['sendAs'] ]
                print('alias encontrados : {} '.format(aliases))


                if alias['sendAsEmail'] not in aliases:
                    print('creando alias')
                    r = gmail.users().settings().sendAs().create(userId='me', body=alias).execute()
                    ds = cls._crearLog(r)
                    session.add(ds)
                    session.commit()

            except Exception as e:
                print(e)

        finally:
            session.close()
