import asyncio
import urllib.parse
from datetime import datetime

import aiohttp
import requests

import utils

FILTERS_STONE = {'filters': [{'key': 'ItemsPerPage', 'value': '36'}], 'page': 1, 'sortCode': 5, 'path': 'Jewelry-Rings-2·Stone-Rings'}
FILTERS_ADJUSTABLE = {'filters': [{'key': 'ItemsPerPage', 'value': '36'}], 'page': 1, 'sortCode': 5, 'path': 'Jewelry-Rings-Adjustable'}
NOT_FAMILY_API_PATH = 'https://jewelers.services/productcore/api/pd/--/'
FAMILY_API_PATH = 'https://jewelers.services/productcore/api/family/'


async def get_request_with_json_response(
        session: aiohttp.ClientSession, url: str
    ) -> dict:
    """
    Запрос и получение информации о товаре в JSON формате.
    """
    async with session.get(url) as response:
        return await response.json()


def post_request(url: str, filters: dict) -> dict:
    """
    Post запрос для получения списка всех товаров на странице.
    """
    response = requests.post(url, json=filters)
    return response.json()


async def query_links(links: list) -> list:
    """Ассинхронный запрос на несколько адресов."""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for link in links:
            tasks.append(get_request_with_json_response(session, link))

        results = await asyncio.gather(*tasks)
        return results


async def responses_to_get_ring_data(rings: list) -> list:
    """Запуск асинхронных запросов на несколько адресов."""
    print('Начинаю делать запросы')
    rings_data = await query_links(rings)
    return rings_data


async def extract_all_info_about_rings(rings_data: list) -> list:
    """
    Получение всех возможных ссылок для товаров
    и возращение запросов по ним.
    """
    links_list = []
    for ring in rings_data:
        if utils.is_family(ring):
            family = utils.generate_family_ring_links(ring)
            links_list.extend(family)
        if utils.is_not_family(ring):
            not_family = utils.generate_ring_links(ring)
            links_list.extend(not_family)
    data = await query_links(links_list)
    print('Получил всю информацию о кольцах')
    return data


def generate_parameters() -> str:
    """Генерация параметров для добавления к ссылке при запросе."""
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime(
        '%a %b %d %Y %H:%M:%S GMT%z (%Z)'
    )
    encoded_datetime = urllib.parse.quote(formatted_datetime)
    return f'?v={encoded_datetime}'


def current_paramet_url(url: str) -> str:
    """Генерация ссылки с текущеми парметрами."""
    link = url + generate_parameters()
    return link


def generate_link_for_ring(value: str) -> str:
    """Генерация ссылок для колец."""
    link = f'{NOT_FAMILY_API_PATH}{value}'
    current_params_link = current_paramet_url(link)
    return current_params_link


def generate_family_link_for_ring(value: str) -> str:
    """Генерация ссылок ссылок для колец с типом `family`."""
    link = f'{FAMILY_API_PATH}{value}'
    current_params_link = current_paramet_url(link)
    return current_params_link
