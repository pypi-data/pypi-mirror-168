from .adapters import City, Timezone, CountryCode
from .domain import ICityRepository, ICountryRepository, Country, CityName
from .models import CityModel, CountryModel
from .database import session


class CityRepository(ICityRepository):

    def get_by_name(self, name: str) -> City | None:
        city = session.query(CityModel).filter_by(name=name).first()
        if city:
            return self.to_dataclass(city)

    def to_dataclass(self, model: CityModel) -> City:
        return City(
            id=model.id,
            name=CityName.create(model.name).value,
            timezone=Timezone.create(model.timezone).value,
            latitude=model.latitude,
            longitude=model.longitude,
        )


class CountryRepository(ICountryRepository):

    def get_by_code(self, code: str) -> Country | None:
        country = session.query(CountryModel).filter_by(code=code).first()
        if country:
            return self.to_dataclass(country)

    def all(self) -> list[Country]:
        countries = []
        for country in session.query(CountryModel).all():
            countries.append(self.to_dataclass(country))
        return countries

    def to_dataclass(self, model: CountryModel) -> Country:
        return Country(
            id=model.id,
            code=CountryCode.create(model.code).value,
            name=model.name,
            states=model.states,
            cities=model.cities,
        )
