from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    indicators = Column(String, nullable=True)
    interval = Column(String, nullable=False)
    style = Column(String, nullable=False)
    timezone = Column(String, nullable=False)
    scale = Column(String, nullable=False)
    exchange = Column(String, nullable=False)
    pic_format = Column(String, nullable=False)