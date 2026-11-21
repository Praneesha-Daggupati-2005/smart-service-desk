import json
from pathlib import Path

from domain.repository import AbstractRepository
from domain.service_request import ServiceRequest
from domain.exceptions import RepositoryError


class FileRepository(AbstractRepository):
    """Concrete JSON implementation of the repository contract."""

    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def _load(self):
        if not self.file_path.exists():
            return []

        try:
            if self.file_path.stat().st_size == 0:
                return []
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as exc:
            raise RepositoryError("The repository JSON file is corrupted.") from exc
        except OSError as exc:
            raise RepositoryError("The repository file could not be read.") from exc

        if not isinstance(data, list):
            raise RepositoryError("The repository JSON must contain a list.")

        try:
            return [ServiceRequest.from_dict(entry) for entry in data]
        except (ValueError, KeyError, TypeError) as exc:
            raise RepositoryError("The repository contains invalid request data.") from exc

    def save_all(self, items):
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            data = [item.to_dict() if isinstance(item, ServiceRequest) else item for item in items]
            with self.file_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
        except OSError as exc:
            raise RepositoryError("The repository file could not be written.") from exc

    def get_all(self):
        return self._load()

    def find_by_id(self, item_id):
        for item in self._load():
            if item.request_id == item_id:
                return item
        return None

    def add(self, item):
        items = self._load()
        items.append(item)
        self.save_all(items)

    def update(self, item):
        items = self._load()
        for index, existing in enumerate(items):
            if existing.request_id == item.request_id:
                items[index] = item
                self.save_all(items)
                return
        raise RepositoryError("Request could not be updated because it does not exist.")
