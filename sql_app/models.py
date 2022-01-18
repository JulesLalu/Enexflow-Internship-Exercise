from sqlalchemy import Column, Integer
from sqlalchemy.sql.sqltypes import Float

from database import Base


class Conso_Datapoint(Base):
    __tablename__ = "RTE_DATA"

    timestamp1 = Column(Integer, primary_key=True)
    consommation = Column(Float)

