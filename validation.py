from numpy import log10

from config.path import RUSSIAN_REGIONS_DATA, TIME_SERIES_CONFIRMED_DATA_RUSSIA

from extractor.load import Loader
from model.sarimax_model import SarimaxModel

tests_order = [(1, 2, 1)]


def count_MALE(real, predict):
    return sum(
        abs((log10(real[i] + 1) / (predict[i] + 1))) + abs(log10((real[i] + 1) / (predict[i] + 1)))
        for i in range(5)
    ) / 5


loader = Loader(RUSSIAN_REGIONS_DATA)
model = SarimaxModel()

countries_codes = loader.load_regions_codes()

confirmed_time_series = loader.load_countries_time_series(
    TIME_SERIES_CONFIRMED_DATA_RUSSIA,
    countries_codes,
)

metrics = []

for order in tests_order:
    for country, time_series in confirmed_time_series.items():
        try:
            metric = count_MALE(
                time_series[75:80],  # реальные данные
                model.predict(time_series[:75], order, 5)  # предикт модели
            )
            metrics.append(metric)
            print(country, metric)
        except Exception as exc:
            pass

    print(order, ':', sum(metrics) / len(countries_codes))
