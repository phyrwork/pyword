from typing import Dict, Iterator, MutableMapping, Tuple


class Grid(MutableMapping[Tuple[int, int], str]):
    def __init__(self, size: Tuple[int, int] = (4, 4)):
        self.size = size
        self.chars: Dict[Tuple[int, int], str] = {}

    def __setitem__(self, k: Tuple[int, int], v: str) -> None:
        if 0 > k[0] >= self.size[0] or 0 > k[1] >= self.size[1]:
            raise KeyError(f"{k} not in bounds of {self.size}")
        self.chars[k] = v

    def __delitem__(self, k: Tuple[int, int]) -> None:
        del self.chars[k]

    def __getitem__(self, k: Tuple[int, int]) -> str:
        return self.chars[k]

    def __len__(self) -> int:
        return len(self.chars)

    def __iter__(self) -> Iterator[Tuple[int, int]]:
        """Yield grid co-ords in row, col order."""
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                yield x, y

    def adj(self, to: Tuple[int, int]) -> Iterator[Tuple[Tuple[int, int], str]]:
        for o in {
            (0, 1),
            (-1, 1),
            (-1, 0),
            (-1, -1),
            (0, -1),
            (1, -1),
            (1, 0),
            (1, 1),
        }:
            a = to[0] + o[0], to[1] + o[1]
            if 0 <= a[0] < self.size[0] and 0 <= a[1] < self.size[1]:
                yield a, self[a]
