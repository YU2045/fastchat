from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from api.db import Base


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    user = Column(String(32))
    text = Column(String(1024))
    like = Column(Integer, default=0)
    # like = relationship('Like', back_populates='message', cascade='delete')


# class Like(Base):
#     __tablename__ = 'likes'
#     id = Column(Integer, ForeignKey('messages.id'), primary_key=True)
#     num_likes = Column(Integer, default=0)
#     message = relationship('Message', back_populates='like')
