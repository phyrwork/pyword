from __future__ import annotations

from contextlib import suppress
from typing import Dict, Iterable, Iterator, Mapping, MutableSet, Tuple


class Trie(MutableSet[str]):
    def __init__(self):
        self.ok = False
        self._next: Dict[str, Trie] = {}

    @property
    def next(self) -> Mapping[str, Trie]:
        return self._next

    def node(self, key: str, create: bool = False) -> Trie:
        u = self
        for i, c in enumerate(key):
            try:
                v = u._next[c]
            except KeyError:
                if not create:
                    raise KeyError(f"{key}[{i}] not found")
                v = Trie()
                u._next[c] = v
            u = v
        return u

    def add(self, key: str) -> None:
        self.node(key, create=True).ok = True

    def discard(self, key: str) -> None:
        with suppress(KeyError):
            self.node(key).ok = False

    def contains(self, key: str) -> bool:
        if not isinstance(key, str):
            return False
        try:
            return self.node(key).ok
        except KeyError:
            return False

    def nodes(self) -> Iterator[Tuple[str, Trie]]:
        s = list(self.next.items())
        while s:
            wu = s.pop()
            yield wu
            w, u = wu
            for c, v in u.next.items():
                s.append((w + c, v))

    def size(self) -> int:
        n = 0
        for _ in self.nodes():
            n += 1
        return n

    def keys(self) -> Iterator[str]:
        for w, n in self.nodes():
            if n.ok:
                yield w

    def len(self) -> int:
        n = 0
        for _ in self.keys():
            n += 1
        return n

    def __contains__(self, key: object) -> bool:
        return isinstance(key, str) and self.contains(key)

    __iter__ = keys
    __len__ = len

    @classmethod
    def from_keys(cls, keys: Iterable[str]) -> Trie:
        tr = Trie()
        for key in keys:
            tr.add(key)
        return tr
