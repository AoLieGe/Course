import asyncio
import logging
import aiohttp
from abstract import AbstractCourse
from provider import Provider as CourseProvider
from misc import get_currency_values


class Course(AbstractCourse):
    def __init__(self, currency_data):
        self.data = currency_data
        self.session = aiohttp.ClientSession()
        self.course_provider = CourseProvider(self.session)
        self.is_state_changed = False

    async def listener(self):
        # method listen external requests from http port
        pass

    async def provider(self, delay):
        # method request actual course from external URL
        while True:
            json_data = await self.course_provider.get()
            if not json_data:
                continue

            logging.debug(json_data)
            actual_values = get_currency_values(self.data.course.keys(), json_data)
            print('Course received successfully')
            await asyncio.sleep(60*delay)

    async def informer(self, delay):
        # method show current actual data in console
        pass
