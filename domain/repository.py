from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    """Storage contract; it contains no JSON or database implementation."""

    @abstractmethod
    def save_all(self, items):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def find_by_id(self, item_id):
        pass

    @abstractmethod
    def add(self, item):
        pass

    @abstractmethod
    def update(self, item):
        pass
