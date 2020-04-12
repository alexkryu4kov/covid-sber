import json

import pandas as pd


TIME_SERIES_DATA = '../data/time_series_covid19_confirmed_global.csv'
COUNTRIES_DATA = '../data/countries.csv'


def load_countries(countries_path: str) -> list:
    countries = pd.read_csv(countries_path)
    return list(countries['ccse_name'])


def load_countries_time_series(filename: str, countries_path: str) -> dict:
    """Принимает на вход путь до csv файла.

    Парсит его в словарь вида {'RUS': [1,2,3]}
    """

    countries_dict = {}

    data = pd.read_csv(filename)
    countries = load_countries(countries_path)
    for country in countries:
        countries_dict[country] = data[data['Country/Region'] == country].values.tolist()[0][4:]
    return countries_dict


countries_dict = load_countries_time_series(TIME_SERIES_DATA, COUNTRIES_DATA)

with open('countries_dict.json', 'w') as fp:
    json.dump(countries_dict, fp)
