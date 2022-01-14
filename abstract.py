from abc import ABC, abstractmethod


class AbstractCourse(ABC):
    @abstractmethod
    async def listener(self):
        # method listen external requests from http port
        pass

    @abstractmethod
    async def provider(self, delay):
        # method request actual course from external URL
        pass

    @abstractmethod
    async def informer(self, delay):
        # method show current actual data in console
        pass

