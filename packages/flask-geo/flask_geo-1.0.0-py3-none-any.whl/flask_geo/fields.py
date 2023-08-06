from wtforms import SelectField

from .repositories import CountryRepository


class CountryField(SelectField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        countries = CountryRepository().all()
        self.choices = [(country.code, country.name) for country in countries]
