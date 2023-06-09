import asyncio

import excel_utils
import utils
import web_requests

STONES_URL = 'https://jewelers.services/productcore/api/pl/Jewelry-Rings-2%C2%B7Stone-Rings'
STONES_FILE_NAME = '2_stones_rings_excel.xlsx'

ADJUSTABLE_URL = 'https://jewelers.services/productcore/api/pl/Jewelry-Rings-Adjustable'
ADJUSTABLE_FILE_NAME = 'adjustable_rings.xlsx'


async def stone_main():
    current_url = web_requests.current_paramet_url(STONES_URL)
    response = web_requests.post_request(
        current_url, web_requests.FILTERS_STONE
    )

    links = utils.generate_list_links_stone(response)
    additional_requsts = await web_requests.responses_to_get_ring_data(links)
    rings_data = await web_requests.extract_all_info_about_rings(additional_requsts)
    rings_in_dicts = utils.turn_ring_info_into_dicts(rings_data)

    col = utils.generate_column_titles(rings_in_dicts)

    excel_utils.create_columns_in_excel(col, STONES_FILE_NAME)
    excel_utils.update_excel_data(rings_in_dicts, STONES_FILE_NAME)


async def adjustable_main():
    current_url = web_requests.current_paramet_url(ADJUSTABLE_URL)
    response = web_requests.post_request(
        current_url, web_requests.FILTERS_ADJUSTABLE
    )

    links = utils.generate_links_list_adjustable(response)
    data = await web_requests.responses_to_get_ring_data(links)
    rings_in_dict = utils.turn_ring_info_into_dicts(data)
    columns = utils.generate_column_titles(rings_in_dict)

    excel_utils.create_columns_in_excel(columns, ADJUSTABLE_FILE_NAME)
    excel_utils.update_excel_data(rings_in_dict, ADJUSTABLE_FILE_NAME)


async def run_periodically():
    while True:
        time = input('Введите время для периодичности запросов в секундах: ')
        await asyncio.gather(stone_main(), adjustable_main())
        print(f'Файлы с информацией о кольцах готов, засыпаю на {time}')
        await asyncio.sleep(int(time))


if __name__ == '__main__':
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_periodically())
    except KeyboardInterrupt:
        print('\nПрограмма остановлена')
    except Exception as e:
        print(f'Программа завершена из-за ошибки - {e}')
