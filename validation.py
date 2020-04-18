from numpy import isnan, log10
from numpy.linalg import LinAlgError

from config.path import RUSSIAN_REGIONS_DATA, TIME_SERIES_CONFIRMED_DATA_RUSSIA
from extractor.load import RegionsLoader
from model.sarimax_model import SarimaxModel

tests_order = [(3, 2, 2)]


def count_MALE(real, predict):
    return sum(
        abs((log10(real[i] + 1) / (predict[i] + 1))) + abs(log10((real[i] + 1) / (predict[i] + 1)))
        for i in range(5)
    ) / 5


regions_loader = RegionsLoader(RUSSIAN_REGIONS_DATA)
sarimax_model = SarimaxModel()

regions_data = regions_loader.load_time_series(TIME_SERIES_CONFIRMED_DATA_RUSSIA)

metrics = []

for order in tests_order:
    for country, series in regions_data.items():
        try:
            metric = count_MALE(
                series[81:86],  # реальные данные
                sarimax_model.predict(series[:81], order, 5)  # предикт модели
            )
            if not isnan(metric):
                metrics.append(metric)
            else:
                metrics.append(0.1)
            print(country, metric)
        except LinAlgError:
            pass

    print(order, ':', sum(metrics) / 85)
