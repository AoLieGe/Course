import json
import logging


class CourseProvider:
    def __init__(self, session):
        self.session = session
        self._URL = 'https://www.cbr-xml-daily.ru/daily_json.js'

    async def get(self):
        """get data from URL and return it in text format"""
        async with self.session.get(self._URL) as r:
            if r and r.status == 200:
                try:
                    return json.loads(await r.text())
                except ValueError:
                    logging.exception('Json parsing error')
            else:
                logging.error(f'Course request error, http get status {r.status}')
