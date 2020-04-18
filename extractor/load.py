import pandas as pd


class Loader:
    def __init__(self, countries_path):
        self.countries = pd.read_csv(countries_path)

    def load_regions_codes(self) -> list:
        return list(self.countries['iso_code'])

    def load_regions_names(self) -> list:
        return list(self.countries['csse_province_state'])

    def load_countries_time_series(self, filename: str, countries_codes) -> dict:
        """Принимает на вход путь до csv файла.

        Парсит его в словарь вида {'RUS': [1,2,3]}
        """

        countries_dict = {}

        data = pd.read_csv(filename)
        countries = self.load_regions_names()
        column_russia = 'Province_State'
        for index, country in enumerate(countries):
            countries_dict[countries_codes[index]] = data[data[column_russia] == country].values.tolist()[0][11:]
        return countries_dict
