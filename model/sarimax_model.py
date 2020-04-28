from abc import ABCMeta, abstractmethod
from typing import List, Tuple

import statsmodels.api as sm


class Model(metaclass=ABCMeta):
    """Абстрактный класс для модели."""

    @abstractmethod
    def predict(
        self,
        time_series: List[int],
        order: Tuple[int],
        amount_of_predictions: int
    ) -> List[int]:
        """На вход получается временной ряд и предсказываются будущие значения."""


class SarimaxModel(Model):
    """Класс для ARIMA модели."""
    def __init__(self) -> None:
        """Инициализация модели."""
        self.model = sm.tsa.statespace.SARIMAX

    def predict(
        self,
        time_series: List[int],
        order: Tuple[int],
        amount_of_predictions: int
    ) -> List[int]:
        """
        Получаем на вход временной ряд с историей заболевших.
        Возвращаем прогноз в виде списка.
        Кол-во дней для прогноза передается через amount_of_predictions.
        """

        start_step = len(time_series)
        end_step = start_step + amount_of_predictions
        model = self.model(time_series, order=order).fit(disp=False)
        covid_forecast = model.predict(start_step, end_step)

        return [int(round(elem)) for elem in covid_forecast]
