from abc import ABC, abstractmethod 


class ResourceHandler(ABC):

    @abstractmethod
    def handle(self, name, *args, **kwargs):
        pass
