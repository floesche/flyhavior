from abc import ABC, abstractmethod


class Transformer(ABC):

    @abstractmethod
    def transform(self, line) -> None:
        pass

    @abstractmethod
    def get_keys(self) -> list:
        pass
