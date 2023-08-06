import itertools
import logging

import aiohttp
import asyncio

from igwrapper.clients.exceptions import *

from igwrapper.models import Position

log = logging.getLogger(__name__)

class AIOIGRest:

    def __init__(self, user: str, pwd: str, key: str, base_url: str = 'https://demo-api.ig.com/gateway/deal'):
        self.user = user
        self.pwd = pwd
        self.key = key
        self.base_url = base_url
        self._cst = None
        self._xst = None
        self._ls_url = None
        self._active_account_id = None

    async def __aenter__(self):
        self.headers = await self._get_session_headers()
        self._xst = self.headers['X-SECURITY-TOKEN']
        self._cst = self.headers['CST']
        self._session = aiohttp.ClientSession(headers=self.headers, requote_redirect_url=False)
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
                if r.status >= 400:
                    raise (IGException(f"Server problem: status code: {r.status}, reason: {r.reason}"))
                self._xst = r.headers['X-SECURITY-TOKEN']
                self._cst = r.headers['CST']
                res = await r.json()
                self._ls_url = res['lightstreamerEndpoint']
                self._active_account_id = res['currentAccountId']
                return {
                    **headers,
                    "X-SECURITY-TOKEN": r.headers['X-SECURITY-TOKEN'],
                    "CST": r.headers['CST']
                }

    @staticmethod
    def _api_limit_hit(rsp_txt):
        return 'exceeded-api-key-allowance' in rsp_txt or \
                'exceeded-account-allowance' in rsp_txt or \
                'exceeded-account-trading-allowance' in rsp_txt or \
                'error.public-api.exceeded-account-historical-data-allowance'

    def parse_response(req):
        async def wrapper(*args, **kwargs):
            r = await req(*args, **kwargs)
            text = await r.text()
            if AIOIGRest._api_limit_hit(text):
                raise ApiExceededException(f"API limit hit: {text}")

            if r.status >= 400:
                raise (IGException(f"Server problem: status code: {r.status}, reason: {r.reason} for url: {r.url}"))
            return await r.json()

        return wrapper

    @parse_response
    async def _req(self, action: str, url, headers: dict = None, params: dict = None, payload: dict = None):

        # Only allowed actions in methods
        s = self._session
        methods = {
            'post': s.post,
            'get': s.get,
            'put': s.put,
            'delete': s.post
        }

        if headers is not None: headers = {k: v for (k, v) in headers.items() if v is not None}
        if payload is not None: payload = {k: v for (k, v) in payload.items() if v is not None}
        if params is not None: params = {k: v for (k, v) in params.items() if v is not None}

        if action == 'delete':
            headers = {
            '_method': 'DELETE',
            'Version': '1'
        }

        return await methods[action](url=url, headers=headers, params=params, json=payload)

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

        return await self._req(action='get', url=url, params=params)

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

        return await self._req(action = 'get', url=url, params=params, headers=headers)

    async def confirm_trade(self, deal_reference):
        log.info("Confirming trade %s", deal_reference)
        url = f'{self.base_url}/confirms/{deal_reference}'

        headers = {
            'Version': '1'
        }

        return await self._req(action='get', url=url, headers=headers)

    async def open_position(self, position: Position, attempts: int=5):
        log.info("Opening position for %s", position.epic)

        url = f'{self.base_url}/positions/otc'

        # TODO fix this ting
        position_obj = position.get_opening_details()

        for i in range(1, attempts):

            try:

                r = await self._req(action='post', url=url, payload=position_obj)
                # Give small amount of time for ig systems to update
                await asyncio.sleep(0.3)

                # TODO convert these to objects
                confirm = await self.confirm_trade(r['dealReference'])

                if confirm['status'] == "OPEN":
                    log.debug("Opened position %s", position.epic)
                    position.is_open = True
                    position.level = confirm['level']
                    return position
            except IGException as e:
                log.error(f"Failed to open position for {position.epic}, attempt {i}")
                continue

        log.error("Failed to open position: %s", position.epic)
        return
    
    async def open_positions(self, positions, attempts: int=5):
        r = await asyncio.gather(*map(self.open_position, positions, itertools.repeat(attempts)))
        return r

    async def get_open_positions(self):
        log.info("Getting all currently open positions")
        url = f'{self.base_url}/positions'

        r = await self._req(action = 'get', url = url)

        return [Position.from_json_get_position_market(p, True) for p in r['positions']]
    
    async def close_position(self, position: Position, attempts: int=5):

        if position is None: return

        log.info("Closing position %s", position.epic)

        url = f'{self.base_url}/positions/otc'

        close_details = position.get_closing_details(position.bid - 0.1)

        log.info("Closing position: %s", {close_details['epic']})

        for _ in range(1, attempts):

            close = await self._req(action='delete', url=url, payload=close_details)

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

    async def search_markets(self, search_str: str):
        log.info('Searching for: %s', search_str)
        url = f'{self.base_url}/markets'

        params = {
            'searchTerm': search_str
        }

        headers = {
            'Version': '1'
        }

        return await self._req(action = 'get', url=url, headers=headers, params=params)
