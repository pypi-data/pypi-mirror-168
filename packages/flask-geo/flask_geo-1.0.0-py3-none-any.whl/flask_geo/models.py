from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class CountryModel(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    code = Column(String(2), nullable=False, unique=True)
    name = Column(String, nullable=False)
    cities = relationship('CityModel', backref='country', lazy=True)
    states = relationship('StateModel', backref='country', lazy=True)


class StateModel(Base):
    __tablename__ = 'state'
    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    cities = relationship('CityModel', backref='state', lazy=True)
    country_id = Column(Integer, ForeignKey('country.id'), nullable=False)


class CityModel(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    timezone = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    country_id = Column(Integer, ForeignKey('country.id'), nullable=False)
    state_id = Column(Integer, ForeignKey('state.id'), nullable=False)
