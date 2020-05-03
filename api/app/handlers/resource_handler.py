from abc import ABC, abstractmethod 


class ResourceHandler(ABC):

    @abstractmethod
    def handle(self, tokenized_message):
        pass
