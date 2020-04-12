from datetime import date
from random import random

from config import COUNTRIES_DATA, SUBMISSION_PATH, TIME_SERIES_CONFIRMED_DATA, TIME_SERIES_DEATHS_DATA
from extractor.load import load_countries_codes, load_countries_time_series
from extractor.save import save_predicts_to_csv


START_DATE = date(2020, 4, 5)
END_DATE = date(2020, 12, 31)

model = ''  # модель загружается откуда-то или импортируется класс с моделью

cases_predicts = {}
death_predicts = {}


def predict(model, time_series: list) -> list:
    """Принимает на вход список с данными и возвращает список предиктов."""

    return [random()]*271


confirmed_time_series = load_countries_time_series(TIME_SERIES_CONFIRMED_DATA, COUNTRIES_DATA)

for country, time_series in confirmed_time_series.items():
    cases_predicts[country] = predict(model, time_series)  # делаем предикт для каждой страны

death_time_series = load_countries_time_series(TIME_SERIES_DEATHS_DATA, COUNTRIES_DATA)

for country, time_series in death_time_series.items():
    death_predicts[country] = predict(model, time_series)  # делаем предикт для каждой страны

countries_codes = load_countries_codes(COUNTRIES_DATA)

save_predicts_to_csv(cases_predicts, death_predicts, countries_codes, SUBMISSION_PATH, START_DATE, END_DATE)
