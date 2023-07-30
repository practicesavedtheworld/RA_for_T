from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, relationship

from app.backend.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(primary_key=True, nullable=False)
    username: Mapped[str] = Column(type_=String(50))
    hashed_password: Mapped[str]

    targets = relationship("Targets", back_populates="user")
