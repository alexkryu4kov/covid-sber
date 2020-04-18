from abc import ABCMeta, abstractmethod

import pandas as pd


class Loader(metaclass=ABCMeta):
    """Класс для загрузки данных и преобразования их в необходимый формат."""

    def __init__(self, info_path: str) -> None:
        self.info = pd.read_csv(info_path)

    @abstractmethod
    def load_time_series(self, time_series_path: str) -> dict:
        """Принимает на вход путь до csv файла.

        Парсит его в словарь вида {'RUS': [1,2,3]}
        """


class CountriesLoader(Loader):

    def __init__(self, countries_info_path: str, countries_with_colonies: tuple):
        super().__init__(countries_info_path)
        self.countries_with_colonies = countries_with_colonies

    def load_time_series(self, time_series_path: str) -> dict:
        countries_dict = {}

        time_series = pd.read_csv(time_series_path)
        codes = list(self.info['iso_alpha3'])
        countries = list(self.info['ccse_name'])

        for index, country in enumerate(countries):
            if country in self.countries_with_colonies:
                countries_dict[codes[index]] = time_series[time_series['Country/Region'] == country].sum().values.tolist()[3:]
            else:
                countries_dict[codes[index]] = time_series[time_series['Country/Region'] == country].values.tolist()[0][4:]
        return countries_dict


class RegionsLoader(Loader):
    def __init__(self, countries_info_path: str):
        super().__init__(countries_info_path)

    def load_time_series(self, time_series_path: str) -> dict:
        regions_dict = {}

        time_series = pd.read_csv(time_series_path)
        codes = list(self.info['iso_code'])
        regions = list(self.info['csse_province_state'])

        for index, region in enumerate(regions):
            regions_dict[codes[index]] = time_series[time_series['Province_State'] == region].values.tolist()[0][11:]
        return regions_dict
