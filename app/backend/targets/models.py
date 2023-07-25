from datetime import datetime

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, String, DateTime, Null, ForeignKey, Integer

from app.backend.database import Base


class Targets(Base):
    __tablename__ = 'targets'

    id: Mapped[int] = Column(type_=Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = Column(ForeignKey('users.id'), nullable=False, type_=Integer)
    title: Mapped[str] = Column(type_=String(50), nullable=False)
    description: Mapped[str] = Column(type_=String(200))
    created_at: Mapped[DateTime] = Column(type_=DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[DateTime] = Column(type_=DateTime, nullable=True, default=Null)
    deleted_at: Mapped[DateTime] = Column(type_=DateTime, nullable=True, default=Null)

    user = relationship('Users', back_populates='targets')
