import sys
import aiohttp
import asyncio
import contextlib
import json
import logging
from aiohttp import web
from data.model import CurrencyData
from data.provider import CourseProvider
from server.abstract import AbstractServer
from data.misc import get_currency_values


class CourseServer(web.Application, AbstractServer):
    def __init__(self, data: CurrencyData, provide_delay: "delay (min) for course requests"):
        super().__init__()
        self.data = data
        self.PROVIDE_DELAY = provide_delay
        self.CUR_URL = 'https://www.cbr-xml-daily.ru/daily_json.js'
        self.init_server()

    def start(self, ip: str, port: int) -> None:
        """start server"""

        # without this app get "RuntimeError: Event loop is closed" on exit (python 3.9 win 10 x64)
        # solution from https://github.com/encode/httpx/issues/914
        if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        web.run_app(self, host=ip, port=port)

    def init_server(self) -> None:
        """init server instance"""
        self.init_routes()
        self.cleanup_ctx.append(self.client_session)
        self.queue_tasks()

    # ===================initialisation methods===========================
    def init_routes(self) -> None:
        """set all required routes for server"""
        routes = [
            web.get('/amount/get', self.get_amount),
            web.post('/amount/set', self.set_modify),
            web.post('/modify', self.set_modify),
            web.get('/{currency}/get', self.get_currency),
        ]

        self.add_routes(routes)

    def queue_tasks(self) -> None:
        """queue client tasks"""
        self.cleanup_ctx.append(self.provide_task)
        self.cleanup_ctx.append(self.inform_task)

    async def client_session(self, app: web.Application) -> None:
        """create client session object"""
        self['client_session'] = session = aiohttp.ClientSession()
        yield
        await session.close()

    # ===================client task starters===========================
    async def provide_task(self, app: web.Application) -> None:
        """run long-lived task, used to start in app.cleanup_ctx"""
        task = asyncio.create_task(self.provide_course())
        yield
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task

    async def inform_task(self, app: web.Application) -> None:
        """run long-lived task, used to start in app.cleanup_ctx"""
        task = asyncio.create_task(self.inform())
        yield
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task

    # ===================server route methods===========================
    async def get_amount(self, request: web.Request) -> web.Response:
        """route method, response with all course data"""
        logging.debug(f'Received request: /amount/get')
        data = self.data.get_all()
        logging.debug(f'Sending response: {data}')
        return web.Response(text=data, headers={'content-type': 'text/plain'}, status=200)

    async def set_modify(self, request: web.Request) -> web.Response:
        """route method, set/modify currency funds"""
        text = await request.text()
        rel_url = str(request.rel_url)
        logging.debug(f"Received request: '{rel_url}' with data: {text}")

        data, *comment = text.split('//')
        try:
            formatted_data = data.strip().replace("'", '"')
            json_data = json.loads(formatted_data)

            if 'modify'.lower() in rel_url.lower():
                funds = self.data.funds
                json_data = {c.upper(): funds[c.upper()] + f for c, f in json_data.items()
                             if c.upper() in funds.keys()}

            self.data.set_funds(json_data)
            result = 'Funds set success'
            status = 200
            logging.debug(f'Sending response: {result}')
        except ValueError:
            result = 'incorrect request format'
            status = 400
            logging.exception(f'Exception: {result}')

        return web.Response(text=result, headers={'content-type': 'text/plain'}, status=status)

    async def get_currency(self, request: web.Request) -> web.Response:
        """route method, get currency course value"""
        currency = request.match_info.get('currency', '')
        logging.debug(f'Received request: /{currency}/get')
        course = self.data.course[currency.upper()]
        response_text = f'{currency}: {course}'
        logging.debug(f'Sending response: {response_text}')
        return web.Response(text=response_text, headers={'content-type': 'text/plain'}, status=200)

    # ===================client task methods===========================
    async def provide_course(self) -> None:
        """get json data from external URL and save it"""
        provider = CourseProvider(self['client_session'])

        while True:
            json_data = await provider.get()
            if not json_data:
                continue

            logging.debug(json_data)
            actual_values = get_currency_values(self.data.course.keys(), json_data)
            if not actual_values:
                continue

            self.data.set_course(actual_values)
            print('Message: Course received successfully')
            await asyncio.sleep(60 * self.PROVIDE_DELAY)  # !!!! convert delay to seconds

    async def inform(self):
        """show current actual data in console if they have updates"""
        while True:
            if self.data.is_data_changed:
                self.data.is_data_changed = False
                print(f'Message: Actual funds, course and funds sum data:\n{self.data.get_all()}\n')
            await asyncio.sleep(60)
