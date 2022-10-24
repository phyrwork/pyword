import sys
from typing import Dict, Iterator, List, MutableMapping, Optional, TextIO, Tuple

import click

from .trie import Node


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


Path = Tuple[Tuple[int, int], ...]


def solve(dct: Node[str], g: Grid) -> Iterator[Tuple[str, Path]]:
    # Seed search with words starting with chars at each grid position.
    s: List[Tuple[Path, Node]] = [
        ((c,), u) for c in g if (u := dct.next.get(g[c])) is not None
    ]
    while s:
        p, u = s.pop()
        # Solution if is a word.
        if u.ok:
            # Extract word from grid using path.
            yield "".join(g[c] for c in p), p
        # Extend search with next chars from unused adjacent.
        for c, w in g.adj(p[-1]):
            if c not in p and (v := u.next.get(w)) is not None:
                s.append(((*p, c), v))


def score(w: str) -> int:
    if len(w) < 3:
        return 0
    if len(w) in (3, 4):
        return 1
    if len(w) == 5:
        return 2
    if len(w) == 6:
        return 3
    if len(w) == 7:
        return 4
    return 11


@click.command()
@click.option("--dictionary", "-d", type=click.File("r"), envvar="PYWORD_DICTIONARY")
@click.argument("rows", type=str, nargs=-1)
def cli(dictionary: Optional[TextIO], rows: List[str]) -> None:
    if dictionary is None:
        raise Exception("no dictionary provided")
    if not rows:
        raise Exception("no grid provided")

    # Replace Qu with just Q to make this game character compatible with our trie.
    def strip(w: str) -> str:
        return w.strip().lower().replace("qu", "q")

    def unstrip(w: str) -> str:
        return w.replace("q", "qu")

    rows = [strip(row) for row in rows]
    if len({len(row) for row in rows}) != 1:
        raise Exception("uneven row sizes")
    w, h = len(rows[0]), len(rows)

    g = Grid(size=(w, h))
    for x, y in g:
        g[x, y] = rows[y][x]

    print("loading dictionary...", end="", file=sys.stderr, flush=True)
    dct = Node.from_keys(map(strip, dictionary))
    print(f" ok ({len(dct)} words, {dct.size()} nodes)", file=sys.stderr, flush=True)

    def process(word: str, path: Path) -> Tuple[str, Path, int]:
        word = unstrip(word)
        return word, path, score(word)

    result = sorted(
        (process(word, path) for word, path in solve(dct, g)),
        key=lambda item: item[2],
        reverse=True,
    )

    for word, path, points in result:
        print(word, path, points)

    uniques = {(word, points) for word, _, points in result}
    max_points = sum(points for _, points in uniques)
    print(f"({len(uniques)} words, {len(result)} paths, {max_points} points)")


if __name__ == "__main__":
    cli()
