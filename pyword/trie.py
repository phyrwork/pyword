from __future__ import annotations

from typing import (
    Dict,
    Generic,
    Hashable,
    Iterable,
    Iterator,
    List,
    Literal,
    MutableSet,
    Sequence,
    Tuple,
    Type,
    TypeVar,
)

H = TypeVar("H", bound=Hashable)


class Node(Generic[H]):
    def __init__(self) -> None:
        self.ok = False
        self.next: Dict[H, Node] = {}

    # Override __len__
    def __bool__(self) -> Literal[True]:
        return True

    def node(self, key: Iterable[H]) -> Node[H] | None:
        u = self
        for c in key:
            if v := u.next.get(c):
                u = v
            else:
                return None
        return u

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

    def add(self, key: Iterable[H]) -> None:
        u = self
        for c in key:
            v = u.next.get(c)
            if not v:
                v = Node()
                u.next[c] = v
            u = v
        u.ok = True

    def remove(self, key: Iterable[H]) -> None:
        if v := self.node(key):
            v.ok = False

    def keys(self) -> Iterator[Sequence[H]]:
        for w, n in self.nodes():
            if n.ok:
                yield w

    def __len__(self) -> int:
        return sum(1 for _ in self.keys())

    def size(self) -> int:
        return sum(1 for _ in self.nodes())

    def search(self, key: Sequence[H]) -> Iterator[Tuple[Sequence[H], Node[H]]]:
        for prefix, u in self.nodes():
            if v := u.node(key):
                yield (*prefix, *key), v

    @classmethod
    def from_keys(cls: Type[Node[H]], keys: Iterable[Sequence[H]]) -> Node[H]:
        u: Node[H] = Node()
        for key in keys:
            u.add(key)
        return u


class Set(MutableSet[Sequence[H]]):
    def __init__(self, root: Node | None = None):
        self.root = root or Node()

    def add(self, key: Iterable[H]) -> None:
        self.root.add(key)

    def discard(self, key: Iterable[H]) -> None:
        self.root.remove(key)

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, Iterable):
            return False
        if v := self.root.node(key):
            return v.ok
        return False

    def __len__(self) -> int:
        return len(self.root)

    def __iter__(self) -> Iterator[Sequence[H]]:
        return self.root.keys()

    @classmethod
    def from_keys(cls: Type[Set[H]], keys: Iterable[Sequence[H]]) -> Set[H]:
        return Set(Node.from_keys(keys))
