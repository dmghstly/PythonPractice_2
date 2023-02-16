"""
Запуск приложения.
"""

from terminaltables import AsciiTable
from termcolor import colored
import asyncclick as click

import pytz, timezonefinder
from datetime import datetime

from reader import Reader
from renderer import Renderer


def get_time(timezone_str: str) -> str:
    """
    Получение текущего времени, исходя из временной зоны

    :return:
    """

    return datetime.now(pytz.timezone(timezone_str)).strftime("%H:%M:%S")


def get_timezone(long: float, lat: float) -> str:
    """
    Получение временной зоны в формате Страна/Город.

    :return:
    """

    tf = timezonefinder.TimezoneFinder()
    return tf.certain_timezone_at(lat=lat, lng=long)


@click.command()
@click.option(
    "--location",
    "-l",
    "location",
    type=str,
    help="Страна и/или город",
    prompt="Страна и/или город",
)
async def process_input(location: str) -> None:
    """
    Поиск и вывод информации о стране, погоде и курсах валют.

    :param str location: Страна и/или город
    """

    location_info = await Reader().find(location)

    if location_info:
        location_info.location.timezone = get_timezone(location_info.location.longitude, location_info.location.latitude)
        location_info.location.current_time = get_time(location_info.location.timezone)

        lines = await Renderer(location_info).render()

        table = AsciiTable(lines)
        table.inner_row_border = True
        print(colored(table.table, 'green'))

    else:
        click.secho("Информация отсутствует.", fg="yellow")


if __name__ == "__main__":
    # запуск обработки входного файла
    # pylint: disable=E1120
    process_input(_anyio_backend="asyncio")
