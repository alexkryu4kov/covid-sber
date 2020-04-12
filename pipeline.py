from datetime import date

from config import COUNTRIES_DATA, SUBMISSION_PATH, TIME_SERIES_CONFIRMED_DATA, TIME_SERIES_DEATHS_DATA
from extractor.load import load_countries_codes, load_countries_time_series
from extractor.save import save_predicts_to_csv
import statsmodels.api as sm

START_DATE = date(2020, 4, 5)
END_DATE = date(2020, 12, 31)

model = sm.tsa.statespace.SARIMAX
order = (1, 2, 1)  # параметры для confirmed

order_death = (3, 2, 2)  # параметры для deaths

cases_predicts = {}
death_predicts = {}


def predict(model, order: tuple, time_series: list) -> list:
    start_step = len(time_series)
    end_step = start_step + 264  # количество дней которое нужно запредиктить (с 12 апреля)
    model = model(time_series, order=order).fit(disp=False)
    predicted = model.predict(start_step, end_step)

    return [int(round(elem)) for elem in predicted]


confirmed_time_series = load_countries_time_series(TIME_SERIES_CONFIRMED_DATA, COUNTRIES_DATA)
death_time_series = load_countries_time_series(TIME_SERIES_DEATHS_DATA, COUNTRIES_DATA)

for country, time_series in confirmed_time_series.items():
    cases_predicts[country] = predict(model, order, time_series)  # делаем предикт для каждой страны

for country, time_series in death_time_series.items():
    try:
        death_predicts[country] = predict(model, order_death, time_series)  # делаем предикт для каждой страны
    except Exception as exc:
        death_predicts[country] = predict(model, (1, 1, 1), time_series)

countries_codes = load_countries_codes(COUNTRIES_DATA)

save_predicts_to_csv(cases_predicts, death_predicts, countries_codes, SUBMISSION_PATH, START_DATE, END_DATE)
