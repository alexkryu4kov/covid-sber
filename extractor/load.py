import pandas as pd

from config.constants import COUNTRIES_WITH_COLONIES


class Loader:
    def __init__(self, countries_path):
        self.countries = pd.read_csv(countries_path)

    def load_countries_codes(self) -> list:
        return list(self.countries['iso_alpha3'])

    def load_countries_names(self) -> list:
        return list(self.countries['ccse_name'])

    def load_countries_time_series(self, filename: str, countries_codes) -> dict:
        """Принимает на вход путь до csv файла.

        Парсит его в словарь вида {'RUS': [1,2,3]}
        """

        countries_dict = {}

        data = pd.read_csv(filename)
        countries = self.load_countries_names()
        for index, country in enumerate(countries):
            if country in COUNTRIES_WITH_COLONIES:
                countries_dict[countries_codes[index]] = data[data['Country/Region'] == country].sum().values.tolist()[3:]
            else:
                countries_dict[countries_codes[index]] = data[data['Country/Region'] == country].values.tolist()[0][4:]
        return countries_dict
