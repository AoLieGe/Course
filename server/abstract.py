from aiohttp import web
from abc import ABC, abstractmethod


class AbstractServer(ABC):
    @abstractmethod
    async def get_amount(self, request: web.Request) -> web.Response:
        """route method - response with all course data"""
        pass

    @abstractmethod
    async def set_amount(self, request: web.Request) -> web.Response:
        """route method - set currency funds"""
        pass

    @abstractmethod
    async def modify(self, request: web.Request) -> web.Response:
        """route method - modify currency funds"""
        pass

    @abstractmethod
    async def get_currency(self, request: web.Request) -> web.Response:
        """route method - get currency course value"""
        pass

    @abstractmethod
    async def provide_course(self) -> None:
        """get json data from external URL and save it"""
        pass

    @abstractmethod
    async def inform(self) -> None:
        """show current actual data in console if they have updates"""
        pass

