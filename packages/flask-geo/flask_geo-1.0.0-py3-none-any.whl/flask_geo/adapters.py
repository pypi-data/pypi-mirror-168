import pytz
import pycountry
from datetime import datetime

from .domain import ICity
from .utils import IValidator


class City(ICity):

    def get_utcoffset(self) -> str:
        timezone = pytz.timezone(self.timezone)
        return str(timezone.localize(datetime.now()))[-6:]


class TimezoneValidator(IValidator):

    def __init__(self, value: str) -> None:
        self.value = value

    def is_valid(self) -> bool:
        if value in pytz.all_timezones:
            return super().is_valid()
        return False


class CountryCode(IValidator):

    def __init__(self, value) -> None:
        self.value = value

    def is_valid(self) -> bool:
        country_codes = [country.alpha_2 for country in pycountry.countries]
        if value in country_codes:
            return super().is_valid()
        return False
