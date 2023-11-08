from abc import ABC, abstractmethod


class HasherInterface(ABC):

    @abstractmethod
    async def hash_filename(self):
        raise NotImplementedError
