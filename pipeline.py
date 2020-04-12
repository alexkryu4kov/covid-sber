from datetime import date

from config import COUNTRIES_DATA, SUBMISSION_PATH, TIME_SERIES_CONFIRMED_DATA, TIME_SERIES_DEATHS_DATA
from extractor.load import load_countries_codes, load_countries_time_series
from extractor.save import save_predicts_to_csv
import statsmodels.api as sm


START_DATE = date(2020, 4, 5)
END_DATE = date(2020, 12, 31)

model = sm.tsa.statespace.SARIMAX
order = (1, 2, 1)  # параметры для ARIMA

cases_predicts = {}
death_predicts = {}


def predict(model, order: tuple, time_series: list) -> list:
    start_step = len(time_series)
    end_step = start_step + 271
    model = model(time_series, order=order).fit(disp=False)
    predicted = model.predict(start_step, end_step)[1:]

    return [int(round(elem)) for elem in predicted]


def validation(model, order: tuple, time_series: list):
    start_step = len(time_series)
    end_step = start_step + 10
    model = model(time_series, order=order).fit(disp=False)
    predicted = model.predict(start_step, end_step)[1:]

    return [int(round(elem)) for elem in predicted]


confirmed_time_series = load_countries_time_series(TIME_SERIES_CONFIRMED_DATA, COUNTRIES_DATA)

for country, time_series in confirmed_time_series.items():
    cases_predicts[country] = predict(model, order, time_series)  # делаем предикт для каждой страны

death_time_series = load_countries_time_series(TIME_SERIES_DEATHS_DATA, COUNTRIES_DATA)

for country, time_series in death_time_series.items():
    death_predicts[country] = predict(model, order, time_series)  # делаем предикт для каждой страны

countries_codes = load_countries_codes(COUNTRIES_DATA)

save_predicts_to_csv(cases_predicts, death_predicts, countries_codes, SUBMISSION_PATH, START_DATE, END_DATE)
