import itertools

import aiohttp
import asyncio
import logging, logging.config

from igwrapper.models import Position

log = logging.getLogger(__name__)

class AIOIGSession:

    def __init__(self, user: str, pwd: str, key: str, base_url: str = 'https://demo-api.ig.com/gateway/deal'):
        self.user = user
        self.pwd = pwd
        self.key = key
        self.base_url = base_url

    async def __aenter__(self):
        headers = await self._get_session_headers()
        self._session = aiohttp.ClientSession(headers=headers)
        return self
    
    async def __aexit__(self, *err):
        await self._session.close()
        self._session = None

    async def _get_session_headers(self):
        log.info('Creating session')
        url= f'{self.base_url}/session'
        headers = {
            "Version": "2",
            'X-IG-API-KEY': self.key
        }
        payload = {
            "identifier": self.user,
            "password": self.pwd
        }
        async with aiohttp.ClientSession(headers=headers) as client:
            async with client.post(url=url, headers=headers, json=payload) as r:
                return {
                    **headers,
                    "X-SECURITY-TOKEN": r.headers['X-SECURITY-TOKEN'],
                    "CST": r.headers['CST']
                }

    async def get_market_details(self, epics, params_input=None):
        log.info('Getting market details for %s', epics)
        url = f'{self.base_url}/markets'

        params = {
            **params_input
        } if params_input != None else {}

        if isinstance(epics, str):
            params['epics'] = epics
        elif isinstance(epics, list):
            params['epics'] = ",".join(str(epic) for epic in epics)

        async with self._session.get(url, params=params) as r:
            return await r.json()

    async def get_historic_prices(self, epic, resolution, from_date, to_date=None, input_headers=None, page_size=0, page_number=None):
        log.info("Getting historic prices for %s", epic)
        url = f'{self.base_url}/prices/{epic}'

        base_headers = {
            'Version': '3'
        }

        headers = {
            **input_headers,
            **base_headers
        } if input_headers != None else base_headers

        params_base = {
            "resolution": resolution,
            "from" : from_date,
            "to": to_date,
            "pageSize": page_size,
            "pageNumber": page_number
        }

        params = { key: value for key, value in params_base.items() if value is not None }

        async with self._session.get(url, params=params, headers=headers) as r:
            return await r.json()

    async def confirm_trade(self, deal_reference):
        log.info("Confirming trade %s", deal_reference)
        url = f'{self.base_url}/confirms/{deal_reference}'

        headers = {
            'Version': '1'
        }

        async with self._session.get(url, headers=headers) as r:
            return await r.json()
            
    
    async def open_position(self, position: Position, attempts: int=5):
        log.info("Opening position for %s", position.epic)

        url = f'{self.base_url}/positions/otc'

        position_obj = position.get_opening_details()

        for _ in range(1, attempts):

            async with self._session.post(url, json=position_obj) as r:
                open = await r.json()
                await asyncio.sleep(0.3)
    
            confirm = await self.confirm_trade(open['dealReference'])

            if confirm['status'] == "OPEN":
                log.debug("Opened position %s", position.epic)
                position.is_open = True
                position.level = confirm['level']
                return position

        log.error("Failed to open position: %s", position.epic)
        return

    async def open_positions(self, positions, attempts: int=5):
        r = await asyncio.gather(*map(self.open_position, positions, itertools.repeat(attempts)))
        return r

    async def get_open_positions(self):
        log.info("Getting all currently open positions")
        url = f'{self.base_url}/positions'

        async with self._session.get(url) as resp:
            r = await resp.json()
            return [Position.from_json_get_position_market(p, True) for p in r['positions']]

    async def close_position(self, position: Position, attempts: int=5):

        log.info("Closing position %s", position.epic)

        if position is None: return

        url = f'{self.base_url}/positions/otc'

        close_details = position.get_closing_details(position.bid - 0.1)

        log.info("Closing position: %s", {close_details['epic']})

        headers = {
            '_method': 'DELETE',
            'Version': '1'
        }

        for _ in range(1, attempts):

            async with self._session.post(url, headers=headers, json=close_details) as resp:
                close = await resp.json()
            await asyncio.sleep(0.3)

            close_conf = await self.confirm_trade(close['dealReference'])

            if close_conf['status'] == "CLOSED":
                position.level = close_conf['level']
                position.is_open = False
                return position

        log.error("Failed to close position %s", position.epic)

    async def close_positions(self, positions, attempts: int=5):
        r = await asyncio.gather(*map(self.close_position, positions, itertools.repeat(attempts)))
        return r