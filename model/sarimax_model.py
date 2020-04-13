from config.constants import ACTUAL_AMOUNT_OF_PREDICTIONS

import statsmodels.api as sm


class Model:
    def __init__(self):
        self.model = sm.tsa.statespace.SARIMAX

    def predict(self, time_series, order):
        start_step = len(time_series)
        end_step = start_step + ACTUAL_AMOUNT_OF_PREDICTIONS
        model = self.model(time_series, order=order).fit(disp=False)
        predicted = model.predict(start_step, end_step)

        return [int(round(elem)) for elem in predicted]
