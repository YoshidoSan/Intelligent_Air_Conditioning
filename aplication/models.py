from sqlalchemy import Boolean, Column, Integer, Numeric, Time, String
from database import Base

# definiowanie tabel w bazie danych


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    time_start = Column(String)
    time_end = Column(String)
    temperature = Column(String)
    humidity = Column(String)


class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True, index=True)
    turned_on = Column(Boolean)


class Continuous(Base):
    __tablename__ = "continuous"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(String)
    humidity = Column(String)
    turned_on = Column(Boolean)


class Tuning(Base):
    __tablename__ = "tuning"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Boolean)
    turned_on_temp = Column(Boolean)
    humidity = Column(Boolean)
    turned_on_hum = Column(Boolean)


