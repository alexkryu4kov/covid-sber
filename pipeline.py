from datetime import date

from config.constants import ACTUAL_AMOUNT_OF_PREDICTIONS
from config.path import COUNTRIES_DATA, SUBMISSION_PATH, TIME_SERIES_CONFIRMED_DATA, TIME_SERIES_DEATHS_DATA
from extractor.load import Loader
from extractor.save import Saver
from model.sarimax_model import SarimaxModel


START_DATE = date(2020, 4, 5)
END_DATE = date(2020, 12, 31)

order = (1, 2, 1)  # параметры для confirmed
order_death = (3, 2, 2)  # параметры для deaths
order_default = (1, 1, 1)


class Predictor:
    def __init__(self, loader, saver, model):
        self.loader = loader
        self.saver = saver
        self.model = model
        self.countries_codes = None
        self.confirmed_data = None
        self.death_data = None

    def load_data(self, confirmed_data, deaths_data):
        self.countries_codes = self.loader.load_countries_codes()
        self.confirmed_data = self.loader.load_countries_time_series(confirmed_data, self.countries_codes)
        self.death_data = self.loader.load_countries_time_series(deaths_data, self.countries_codes)

    def predict_confirmed(self):
        cases_predicts = {}
        for country, time_series in self.confirmed_data.items():
            cases_predicts[country] = self.model.predict(
                time_series,
                order,
                ACTUAL_AMOUNT_OF_PREDICTIONS
            )
        return cases_predicts

    def predict_deaths(self):
        death_predicts = {}
        for country, time_series in self.death_data.items():
            try:
                death_predicts[country] = self.model.predict(
                    time_series,
                    order_death,
                    ACTUAL_AMOUNT_OF_PREDICTIONS
                )
            except Exception as exc:
                death_predicts[country] = self.model.predict(
                    time_series,
                    order_default,
                    ACTUAL_AMOUNT_OF_PREDICTIONS
                )
        return death_predicts

    def save_predicts(self, cases_predicts, death_predicts, submission_path):
        self.saver.predicts_to_csv(
            cases_predicts,
            death_predicts,
            self.countries_codes,
            submission_path,
        )

    def facade(self, confirmed_data, deaths_data, submission_path):
        self.load_data(confirmed_data, deaths_data)
        cases_predicts = self.predict_confirmed()
        death_predicts = self.predict_deaths()
        self.save_predicts(cases_predicts, death_predicts, submission_path)


loader = Loader(COUNTRIES_DATA)
saver = Saver(START_DATE, END_DATE)
model = SarimaxModel()

predictor = Predictor(loader, saver, model)
predictor.facade(TIME_SERIES_CONFIRMED_DATA, TIME_SERIES_DEATHS_DATA, SUBMISSION_PATH)
