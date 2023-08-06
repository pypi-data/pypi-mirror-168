from abc import ABC, abstractmethod, abstractstaticmethod
from dataclasses import dataclass
import re

from .utils import IValidator


class CityName(IValidator):

    def is_valid(self) -> bool:
        city_name_re = re.compile(r'^\D+, \D+$')
        if city_name_re.findall(value):
            return super().is_valid()
        return False


@dataclass
class ICity(ABC):
    id: int
    name: CityName
    timezone: IValidator
    latitude: float
    longitude: float

    @abstractmethod
    def get_utcoffset(self) -> str:
        raise NotImplementedError()


class ICityRepository(ABC):

    @abstractmethod
    def get_by_name(self, name: str) -> ICity | None:
        raise NotImplementedError()


@dataclass
class State:
    code: str
    name: str
    cities: list[ICity]


@dataclass
class Country:
    code: IValidator
    name: str
    states: list[State]
    cities: list[ICity]


class ICountryRepository(ABC):

    @abstractmethod
    def get_by_code(self, code: str) -> Country | None:
        raise NotImplementedError()

    @abstractmethod
    def all(self) -> list[Country]:
        raise NotImplementedError()
