from config import ACTUAL_AMOUNT_OF_PREDICTIONS, TOTAL_AMOUNT_OF_PREDICTIONS

import pandas as pd
from dateutil.rrule import rrule, DAILY

NUMBER_OF_ZERO_PREDICTIONS = TOTAL_AMOUNT_OF_PREDICTIONS - ACTUAL_AMOUNT_OF_PREDICTIONS - 1


class Saver:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def iterate_over_dates(self) -> list:
        dates = []
        for dt in rrule(DAILY, dtstart=self.start_date, until=self.end_date):
            dates.append(dt.strftime("%Y-%m-%d"))
        return dates

    def predicts_to_csv(
            self,
            cases_predicts: dict,
            death_predicts: dict,
            countries_codes: list,
            path_to_save: str,
    ) -> None:
        """Берет словарь вида {'RUS': [1,2,3]} и сохраняет в нужном формате в csv."""

        dates = self.iterate_over_dates()
        all_data = []
        for code in countries_codes:
            data = pd.DataFrame()
            data['date'] = dates
            data['country'] = [code] * TOTAL_AMOUNT_OF_PREDICTIONS
            data['prediction_confirmed'] = [0] * NUMBER_OF_ZERO_PREDICTIONS + cases_predicts[code]
            data['prediction_deaths'] = [0] * NUMBER_OF_ZERO_PREDICTIONS + death_predicts[code]
            all_data.append(data)

        full_data = pd.concat(all_data)

        full_data.to_csv(path_to_save, index=False)
