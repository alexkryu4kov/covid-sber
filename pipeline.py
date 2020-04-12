from config import COUNTRIES_DATA, TIME_SERIES_DATA
from extractor.load import load_countries_time_series

model = ''  # модель загружается откуда-то или импортируется класс с моделью

country_predicts = {}


def save_predicts_to_csv(country_predicts: dict) -> None:
    """Берет словарь вида {'RUS': [1,2,3]} и сохраняет в нужном формате в csv."""


def predict(model, time_series: list) -> list:
    """Принимает на вход список с данными и возвращает список предиктов."""


countries_time_series = load_countries_time_series(TIME_SERIES_DATA, COUNTRIES_DATA)

for country, time_series in countries_time_series.items():
    country_predicts[country] = predict(model, time_series)  # делаем предикт для каждой страны

save_predicts_to_csv(country_predicts)
