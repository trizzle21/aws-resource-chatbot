from abc import ABC, abstractmethod 


class ResourceHandler(ABC):

    @abstractmethod
    def handle(self, tokenized_message):
        pass

    @abstractmethod
    def _refresh_resources(self):
        pass

    # def retrieve_intended_resources(self, tokenized_message):
    #     resources: Dict[str, str]
    #     if self.cache.get(self.cache_key):
    #         resources = self.cache.get(self.cache_key)
    #     else:
    #         resources = self._refresh_resources()

    #     resource_names = set(resources.keys())
    #     intended_resources: List = list(resource_names.intersection(tokenized_message))
    #     # TODO: fix to just return list
    #     return intended_resources, resources