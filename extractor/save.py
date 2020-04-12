from datetime import date
from dateutil.rrule import rrule, DAILY

import pandas as pd


def iterate_over_dates(start: date, end: date) -> list:
    dates = []
    for dt in rrule(DAILY, dtstart=start, until=end):
        dates.append(dt.strftime("%Y-%m-%d"))
    return dates


def save_predicts_to_csv(
    country_predicts: dict,
    path_to_save: str,
    start_date: date,
    end_date: date
) -> None:
    """Берет словарь вида {'RUS': [1,2,3]} и сохраняет в нужном формате в csv."""

    dates = iterate_over_dates(start_date, end_date)
    data = pd.DataFrame()
    data['date'] = dates
    data['country'] = ['AFG']*3
    data['prediction_confirmed'] = country_predicts['AFG']

    data.to_csv(path_to_save, index=False)
