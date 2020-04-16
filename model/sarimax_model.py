import statsmodels.api as sm


class SarimaxModel:
    def __init__(self):
        self.model = sm.tsa.statespace.SARIMAX

    def predict(self, time_series, order, amount_of_predictions):
        start_step = len(time_series)
        end_step = start_step + amount_of_predictions
        model = self.model(time_series, order=order).fit(disp=False)
        predicted = model.predict(start_step, end_step)

        return [int(round(elem)) for elem in predicted]
