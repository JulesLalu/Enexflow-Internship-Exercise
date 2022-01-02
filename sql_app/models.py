from sqlalchemy import Column, Integer
from sqlalchemy.sql.sqltypes import Float

from .database import Base


class Conso_Datapoint(Base):
    __tablename__ = "RTE_DATA"

    timestamp = Column(Integer, primary_key=True)
    conso = Column(Float)

