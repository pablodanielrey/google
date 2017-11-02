import logging
logging.getLogger().setLevel(logging.DEBUG)
import os
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, func, and_
from sqlalchemy.orm import joinedload

from model_utils import Base

engine = create_engine('postgresql://{}:{}@{}:5432/{}'.format(
    os.environ['GOOGLE_DB_USER'],
    os.environ['GOOGLE_DB_PASSWORD'],
    os.environ['GOOGLE_DB_HOST'],
    os.environ['GOOGLE_DB_NAME']
), echo=True)
Session = sessionmaker(bind=engine)


import google.model.entities.*
from pprint import pprint

if __name__ == '__main__':
    sileg_url = os.environ['SILEG_API_URL']
    result = session.query(func.max(Sincronizacion.actualizado)).first()
    result = result if result[0] else session.query(func.max(Sincronizacion.creado)).first()
    fecha = result[0]

    logging.info('fecha de la ultima actualizacion : {}'.format(fecha))

    q = '{}{}'.format(cls.sileg_url, '/usuarios/')
    params = {'c':True}
    if fecha:
        params['f'] = fecha - datetime.timedelta(hours=24)
    else:
        params['f'] = datetime.datetime.now() - datetime.timedelta(days=9000)

    resp = requests.get(q, params=params)
    usuarios = []
    if resp.status_code == 200:
        susuarios = resp.json()
        usuarios = [u['usuario'] for u in susuarios]

    pprint(usuarios)
