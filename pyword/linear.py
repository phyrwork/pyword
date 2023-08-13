import sys
from functools import cached_property
from itertools import product
from typing import Iterator, List, Mapping, Sequence, Set, TextIO, Tuple

import click
from typing_extensions import TypeAlias

from . import trie

YX: TypeAlias = Tuple[int, int]


def yx_add(a: YX, b: YX) -> YX:
    ya, xa = a
    yb, xb = b
    return ya + yb, xa + xb


class Grid(Mapping[YX, str]):
    def __init__(self, *rows: str) -> None:
        row_sizes = {len(row) for row in rows}
        if len(row_sizes) < 1:
            raise ValueError(
                f"all rows must be the same size: got sizes {sorted(row_sizes)}"
            )
        self._rows = tuple(rows)

    @cached_property
    def size(self) -> YX:
        if len(self._rows) == 0:
            return 0, 0
        return len(self._rows), len(self._rows[0])

    def __getitem__(self, yx: YX) -> str:
        if yx not in self:
            raise KeyError(yx)
        return self._rows[yx[0]][yx[1]]

    def __len__(self) -> int:
        y, x = self.size
        return y * x

    def __iter__(self) -> Iterator[YX]:
        y, x = self.size
        return product(range(y), range(x))

    def __contains__(self, yx: object) -> bool:
        if not isinstance(yx, tuple):
            return False
        if len(yx) != 2:
            return False
        y, x = yx
        ymax, xmax = self.size
        return 0 <= y < ymax and 0 <= x < xmax


Word: TypeAlias = Tuple[YX, ...]


ORIENTATIONS: Set[YX] = {
    (0, 1),
    (-1, 1),
    (-1, 0),
    (-1, -1),
    (0, -1),
    (1, -1),
    (1, 0),
    (1, 1),
}


def solve(dct: trie.Node, grid: Grid) -> Iterator[Word]:
    seen: Set[Word] = set()

    todo: List[Tuple[trie.Node, YX, Word]] = []
    for yx0, char0 in grid.items():
        if (v := dct.next.get(char0)) is not None:
            for dyx in ORIENTATIONS:
                todo.append((v, dyx, (yx0,)))
    while todo:
        u, dyx, path = todo.pop()
        if u.ok:
            if path not in seen:
                yield path
                seen.add(path)
        yx0 = path[-1]
        yx1 = yx_add(yx0, dyx)
        if char1 := grid.get(yx1):
            if (v := u.next.get(char1)) is not None:
                todo.append((v, dyx, (*path, yx1)))


@click.command()
@click.option(
    "--dictionary", "-d", "dct_file", type=click.File("r"), envvar="PYWORD_DICTIONARY"
)
@click.argument("rows", type=str, nargs=-1)
def cli(dct_file: TextIO | None, rows: Sequence[str]) -> None:
    grid = Grid(*rows)

    if dct_file is None:
        raise Exception("no dictionary provided")

    print("loading dictionary...", end="", file=sys.stderr, flush=True)
    dct = trie.Node.from_keys(map(str.strip, dct_file))
    print(f" ok ({len(dct)} words, {dct.size()} nodes)", file=sys.stderr, flush=True)

    for path in solve(dct, grid):
        chars = "".join(grid[yx] for yx in path)
        print(chars, path)
