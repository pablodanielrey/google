from sqlalchemy import func, Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from model_utils import Base


class Sincronizacion(Base):
    ''' id es el mismo que el usuario '''

    __tablename__ = 'sincronizacion'
    __table_args__ = ({'schema': 'google'})

    dni = Column(String)
    clave_id = Column(String)
    clave = Column(String)
    clave_actualizada = Column(DateTime)
    sincronizado = Column(DateTime)
    #forzar = Column(Boolean,False)
