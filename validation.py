from numpy import log10

from config.path import COUNTRIES_DATA, TIME_SERIES_CONFIRMED_DATA

from extractor.load import Loader
from model.sarimax_model import SarimaxModel

order = (1, 2, 1)


def count_MALE(real, predict):
    return sum(
        abs((log10(real[i] + 1) / (predict[i] + 1))) + abs(log10((real[i] + 1) / (predict[i] + 1)))
        for i in range(9)
    ) / 9


loader = Loader(COUNTRIES_DATA)
model = SarimaxModel()

countries_codes = loader.load_countries_codes()

confirmed_time_series = loader.load_countries_time_series(
    TIME_SERIES_CONFIRMED_DATA,
    countries_codes,
)

metrics = []

for country, time_series in confirmed_time_series.items():
    try:
        metric = count_MALE(
            time_series[68:78],  # реальные данные
            model.predict(time_series[:68], order, 9)  # предикт модели
        )
        metrics.append(metric)
        print(country, metric)
    except Exception as exc:
        print(exc)

print(metrics)
