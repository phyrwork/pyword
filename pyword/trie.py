from __future__ import annotations

from contextlib import suppress
from typing import (
    Dict,
    Hashable,
    Iterable,
    Iterator,
    List,
    MutableSet,
    Sequence,
    Tuple,
    Type,
    TypeVar,
)

H = TypeVar("H", bound=Hashable)


class Node(MutableSet[Sequence[H]]):
    def __init__(self) -> None:
        self.ok = False
        self.next: Dict[H, Node] = {}

    def node(self, key: Iterable[H], create: bool = False) -> Node[H]:
        u = self
        for i, c in enumerate(key):
            try:
                v = u.next[c]
            except KeyError:
                if not create:
                    raise KeyError(f"{key}[{i}] not found")
                v = type(self)()
                u.next[c] = v
            u = v
        return u

    def add(self, key: Iterable[H]) -> None:
        self.node(key, create=True).ok = True

    def discard(self, key: Iterable[H]) -> None:
        with suppress(KeyError):
            self.node(key).ok = False

    def contains(self, key: Iterable[H]) -> bool:
        try:
            return self.node(key).ok
        except KeyError:
            return False

    def nodes(self) -> Iterator[Tuple[Sequence[H], Node[H]]]:
        s: List[Tuple[Tuple[H, ...], Node[H]]] = [
            ((c,), u) for c, u in self.next.items()
        ]
        while s:
            wu = s.pop()
            yield wu
            w, u = wu
            for c, v in u.next.items():
                s.append(((*w, c), v))

    def search(self, key: Sequence[H]) -> Iterator[Tuple[Sequence[H], Node[H]]]:
        for prefix, node in self.nodes():
            with suppress(KeyError):
                yield prefix, node.node(key)

    def size(self) -> int:
        n = 0
        for _ in self.nodes():
            n += 1
        return n

    def keys(self) -> Iterator[Sequence[H]]:
        for w, n in self.nodes():
            if n.ok:
                yield w

    def len(self) -> int:
        n = 0
        for _ in self.keys():
            n += 1
        return n

    __contains__ = contains  # type: ignore
    __iter__ = keys
    __len__ = len

    @classmethod
    def from_keys(cls: Type[Node[H]], keys: Iterable[Sequence[H]]) -> Node[H]:
        tr: Node[H] = Node()
        for key in keys:
            tr.add(key)
        return tr
