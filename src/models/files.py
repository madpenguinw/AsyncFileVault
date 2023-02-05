from datetime import datetime

from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref, relationship

from db.db import Base


class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=False, nullable=False)
    user_id = Column(UUID, ForeignKey('user.id', ondelete='CASCADE'))
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    path = Column(String(500), unique=False, nullable=False)
    size = Column(Float, unique=False, nullable=False)
    is_downloadable = Column(Boolean, default=True)

    user = relationship('User', back_populates='files')
