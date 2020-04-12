from datetime import date
from dateutil.rrule import rrule, DAILY

import pandas as pd

START_DATE = date(2020, 4, 5)
END_DATE = date(2020, 4, 7)


test_dict = {
    'Albania': [0, 1, 2]
}


def iterate_over_dates(start: date, end: date) -> list:
    dates = []
    for dt in rrule(DAILY, dtstart=start, until=end):
        dates.append(dt.strftime("%Y-%m-%d"))
    return dates


def save_predicts_to_csv(country_predicts: dict, path_to_save: str) -> None:
    """Берет словарь вида {'RUS': [1,2,3]} и сохраняет в нужном формате в csv."""

    dates = iterate_over_dates(START_DATE, END_DATE)
    data = pd.DataFrame()
    data['date'] = dates
    data['country'] = ['Albania']*3
    data['prediction_confirmed'] = country_predicts['Albania']

    data.to_csv(path_to_save)
