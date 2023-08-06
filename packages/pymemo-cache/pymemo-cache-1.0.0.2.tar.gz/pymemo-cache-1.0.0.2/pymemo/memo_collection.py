from typing import Any, Dict, Optional
from datetime import datetime, timedelta

from .memo_item import MemoItem


class MemoCollection:
    __slots__ = [
        '_expiration_interval',
        '_collection',
    ]

    def __init__(self, expiration_interval: Optional[float] = None) -> None:
        self._expiration_interval = expiration_interval
        self._collection: Dict[str, MemoItem] = {}

    @property
    def expiration_interval(self):
        return self._expiration_interval

    @expiration_interval.setter
    def expiration_interval(self, expiration_interval: Optional[float]):
        self._expiration_interval = expiration_interval

    @property
    def length(self):
        return len(self._collection)

    def set_item(
            self, key: str, value, expires_at: Optional[datetime] = None,
            expiration_interval: Optional[float] = None) -> None:
        expiration_interval = expiration_interval if (
            bool(expiration_interval)) else self._expiration_interval

        if not expires_at and bool(expiration_interval):
            expires_at = datetime.now() + timedelta(seconds=expiration_interval)
        self._collection[key] = MemoItem(value, expires_at)

    def get_item(self, key: str) -> Any:
        try:
            return self._collection[key].value
        except KeyError:
            return None
        finally:
            self.clear()

    def delete_item(self, key: str) -> None:
        if key in self._collection:
            del self._collection[key]

    def clear(self, only_expired_items=True) -> None:
        if only_expired_items:
            for key, item in self._collection.copy().items():
                if not item.has_valid_cache():
                    self.delete_item(key)
        else:
            self._collection = {}
