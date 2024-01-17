import re

import requests


PRODUCT_AMOUNT = 10
QUERY_PATTERN = r'^([a-zA-Z]{1,4}):(.+)$'
SEARCH_URL = (
    'https://search.wb.ru/exactmatch/ru/common/v4/search?'
    'appType=1&curr=rub&dest=-1257786'
    '&query={0}&resultset=catalog'
    '&sort=popular&spp=24&suppressSpellcheck=false'
)
WB_PRODUCT_URL = 'https://www.wildberries.ru/catalog/{0}/detail.aspx'
HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'search.wb.ru',
    'Origin': 'https://www.wildberries.ru',
    'Pragma': 'no-cache',
    'Referer': 'https://www.wildberries.ru/',
    'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Gpc': '1',
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    )
}


class Parser:

    def __init__(self) -> None:
        self.processors = {
            'wild': self.__parse_wild_by_kw
        }

    async def parse_by_query(self, query: str):
        match = re.match(QUERY_PATTERN, query)
        source = match.group(1).strip()
        keyword = match.group(2).strip()
        if source not in self.processors:
            raise NotImplementedError(f'Не назначен обработчик на источник {source}')
        return await self.processors[source](keyword, PRODUCT_AMOUNT)

    async def __parse_wild_by_kw(self, kw: str, amount: int):
        response = requests.get(SEARCH_URL.format(kw), headers=HEADERS).json()
        result = []
        if 'data' in response:
            if 'products' in response['data']:
                products = response['data']['products']
                for i in range(min(amount, len(products))):
                    data = products[i]
                    result.append(
                        f'{data['name']} - {WB_PRODUCT_URL.format(data['id'])}'
                    )
        return '\n'.join(result) if result else 'Не найдено товаров по запросу'


parser = Parser()
