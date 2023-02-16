"""
Функции для формирования выходной информации.
"""

from decimal import ROUND_HALF_UP, Decimal

from collectors.models import LocationInfoDTO


class Renderer:
    """
    Генерация результата преобразования прочитанных данных.
    """

    def __init__(self, location_info: LocationInfoDTO) -> None:
        """
        Конструктор.

        :param location_info: Данные о географическом месте.
        """

        self.location_info = location_info

    async def render(self) -> list:
        """
        Форматирование прочитанных данных.

        :return: Результат форматирования
        """

        result = [[f"Информация о стране"],
                  [f"Страна: {self.location_info.location.name}"],
                  [f"Площадь страны: {await self._format_area()} км. кв."],
                  [f"Столица: {self.location_info.location.capital}"],
                  [f"Временная зона столицы: {self.location_info.location.timezone}"],
                  [f"Текущее время в столице: {self.location_info.location.current_time}"],
                  [f"Координааты столицы: {self.location_info.location.longitude} д. {self.location_info.location.latitude} ш."],
                  [f"Регион: {self.location_info.location.subregion}"],
                  [f"Языки: {await self._format_languages()}"],
                  [f"Население страны: {await self._format_population()} чел."],
                  [f"Курсы валют: {await self._format_currency_rates()}"],
                  [f"Информация о погоде"],
                  [f"Погода: {self.location_info.weather.temp} °C"],
                  [f"Описание погоды: {self.location_info.weather.description}"],
                  [f"Видимость: {self.location_info.weather.visibility} м."],
                  [f"Скорость ветра: {self.location_info.weather.wind_speed} м/с"],
                  [f"Топ 3 новости за последнее время из {self.location_info.location.name}"],
                  [f"1. {self.location_info.news.article1}"],
                  [f"2. {self.location_info.news.article2}"],
                  [f"3. {self.location_info.news.article3}"],
        ]

        return result

    async def _format_area(self) -> str:
        """
        Форматирование информации о площади страны.

        :return:
        """

        if (self.location_info.location.area == 0.0):
            return "Нет данных"
        else:
            return int(self.location_info.location.area)

    async def _format_languages(self) -> str:
        """
        Форматирование информации о языках.

        :return:
        """

        return ", ".join(
            f"{item.name} ({item.native_name})"
            for item in self.location_info.location.languages
        )

    async def _format_population(self) -> str:
        """
        Форматирование информации о населении.

        :return:
        """

        # pylint: disable=C0209
        return "{:,}".format(self.location_info.location.population).replace(",", ".")

    async def _format_currency_rates(self) -> str:
        """
        Форматирование информации о курсах валют.

        :return:
        """

        return ", ".join(
            f"{currency} = {Decimal(rates).quantize(exp=Decimal('.01'), rounding=ROUND_HALF_UP)} руб."
            for currency, rates in self.location_info.currency_rates.items()
        )
