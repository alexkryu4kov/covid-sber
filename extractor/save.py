from abc import ABCMeta, abstractmethod
from datetime import date
from typing import List

from config.constants import ACTUAL_AMOUNT_OF_PREDICTIONS, TOTAL_AMOUNT_OF_PREDICTIONS

import pandas as pd
from dateutil.rrule import rrule, DAILY

NUMBER_OF_ZERO_PREDICTIONS = TOTAL_AMOUNT_OF_PREDICTIONS - ACTUAL_AMOUNT_OF_PREDICTIONS - 1


def iterate_over_dates(start_date: date, end_date: date) -> list:
    """Метод, позволяющий получать список дат в заданном интервале."""
    dates = []
    for dt in rrule(DAILY, dtstart=start_date, until=end_date):
        dates.append(dt.strftime("%Y-%m-%d"))
    return dates


class AbstractSaver(metaclass=ABCMeta):
    """Класс для сохранения полученных предсказаний в актуальный формат сабмита."""

    @abstractmethod
    def save(
        self,
        path_to_save: str,
        cases_predicts: List[dict],
        death_predicts: List[dict],
        start_date: date,
        end_date: date
    ) -> None:
        """Метод принимающий список предсказаний и сохраняющий их в csv."""
        pass


class Saver(AbstractSaver):
    def __init__(self):
        pass

    def save(
        self,
        path_to_save: str,
        cases_predicts: List[dict],
        death_predicts: List[dict],
        start_date: date,
        end_date: date
    ) -> None:
        """"""
        dates = iterate_over_dates(start_date, end_date)
        all_data = []
        for i in range(2):
            iteration_data = []
            for code in cases_predicts[i].keys():
                data = pd.DataFrame()
                data['date'] = dates
                data['country'] = [code] * TOTAL_AMOUNT_OF_PREDICTIONS
                data['prediction_confirmed'] = [0] * NUMBER_OF_ZERO_PREDICTIONS + cases_predicts[i][code]
                data['prediction_deaths'] = [0] * NUMBER_OF_ZERO_PREDICTIONS + death_predicts[i][code]
                iteration_data.append(data)
            all_data.append(pd.concat(iteration_data))

        final_data = pd.concat(all_data)
        final_data.to_csv(path_to_save, index=False)
