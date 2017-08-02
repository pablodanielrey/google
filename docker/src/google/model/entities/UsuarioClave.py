from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from model_utils import Base

class UsuarioClave(Base):

    __tablename__ = 'user_password'
    __table_args__ = ({'schema': 'credentials'})

    usuario = Column('username', String)
    clave = Column('password', String)

    usuario_id = Column('user_id', String, ForeignKey('profile.users.id'))
    usuario = relationship('Usuario', back_populates='claves')
