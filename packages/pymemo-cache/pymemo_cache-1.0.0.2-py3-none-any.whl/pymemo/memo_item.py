from typing import Any, Optional
from datetime import datetime


class MemoItem:
    __slots__ = [
        '_value',
        '_expires_at',
    ]

    def __init__(
            self, value: Any, expires_at: Optional[datetime] = None) -> None:
        self._value = value
        self._expires_at = expires_at

    @property
    def value(self):
        if not self.has_valid_cache():
            return None
        return self._value

    def has_valid_cache(self) -> bool:
        if not bool(self._expires_at):
            return True
        return datetime.now() <= self._expires_at
