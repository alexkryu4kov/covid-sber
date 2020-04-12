from datetime import date
from dateutil.rrule import rrule, DAILY

import pandas as pd


def iterate_over_dates(start: date, end: date) -> list:
    dates = []
    for dt in rrule(DAILY, dtstart=start, until=end):
        dates.append(dt.strftime("%Y-%m-%d"))
    return dates


def save_predicts_to_csv(
    cases_predicts: dict,
    death_predicts: dict,
    countries_codes: list,
    path_to_save: str,
    start_date: date,
    end_date: date
) -> None:
    """Берет словарь вида {'RUS': [1,2,3]} и сохраняет в нужном формате в csv."""

    dates = iterate_over_dates(start_date, end_date)
    all_data = []
    for code in countries_codes:
        data = pd.DataFrame()
        data['date'] = dates
        data['country'] = [code]*271
        data['prediction_confirmed'] = cases_predicts[code]
        data['prediction_deaths'] = death_predicts[code]
        all_data.append(data)

    full_data = pd.concat(all_data)

    full_data.to_csv(path_to_save, index=False)
