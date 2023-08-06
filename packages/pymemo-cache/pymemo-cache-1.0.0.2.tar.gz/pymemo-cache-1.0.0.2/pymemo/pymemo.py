from typing import Dict, Optional

from .memo_collection import MemoCollection


class PyMemo:
    __slots__ = [
        '_collections',
    ]

    def __init__(self) -> None:
        self._collections: Dict[str, MemoCollection] = {}

    @property
    def length(self):
        return len(self._collections)

    def __str__(self):
        result = [f'Total collections: {self.length}\n']
        for name, collection in self._collections.items():
            result.append(f'{name} ─ Total items: {collection.length}')
        return '\n'.join(result)

    def create_collection(
            self, name: str,
            expiration_interval: Optional[int] = None) -> MemoCollection:
        if name not in self._collections:
            self._collections[name] = MemoCollection(expiration_interval)
        return self._collections[name]

    def collection(self, name: str) -> MemoCollection:
        try:
            return self._collections[name]
        except KeyError:
            return None

    def delete_collection(self, name: str) -> None:
        if name in self._collections:
            del self._collections[name]

    def clear_collections(self, only_expired_items=True) -> None:
        for collection in self._collections.values():
            collection.clear(only_expired_items)
