from typing import Callable, Dict, Iterable, Sequence, Set, Tuple

from pytest import mark, param

from .boggle import Grid, Path, solve
from .trie import Node

KeyCharFunc = Callable[[Tuple[int, int]], str]


def key_to_char(k: Tuple[int, int]) -> str:
    return f"{k[0]}.{k[1]}"


def unpack_sequences(g: Sequence[Sequence[str]]) -> KeyCharFunc:
    def char(k: Tuple[int, int]) -> str:
        x, y = k
        return g[y][x]

    return char


def init_grid(
    size: Tuple[int, int] = (4, 4),
    chars: KeyCharFunc = key_to_char,
):
    g = Grid(size)
    for k in g:
        g[k] = chars(k)
    return g


class TestGrid:
    @mark.parametrize(
        ["g", "to", "want"],
        [
            param(
                init_grid(size=(3, 3)),
                (1, 1),
                {
                    k: key_to_char(k)
                    for k in {
                        (0, 0),
                        (0, 1),
                        (0, 2),
                        (1, 0),
                        (1, 2),
                        (2, 0),
                        (2, 1),
                        (2, 2),
                    }
                },
                id="middle",
            ),
            param(
                init_grid(size=(3, 3)),
                (0, 0),
                {
                    k: key_to_char(k)
                    for k in {
                        (1, 0),
                        (1, 1),
                        (0, 1),
                    }
                },
                id="bottom_left",
            ),
            param(
                init_grid(size=(3, 3)),
                (2, 0),
                {
                    k: key_to_char(k)
                    for k in {
                        (1, 0),
                        (1, 1),
                        (2, 1),
                    }
                },
                id="bottom_right",
            ),
            param(
                init_grid(size=(3, 3)),
                (2, 2),
                {
                    k: key_to_char(k)
                    for k in {
                        (1, 2),
                        (1, 1),
                        (2, 1),
                    }
                },
                id="top_right",
            ),
            param(
                init_grid(size=(3, 3)),
                (0, 2),
                {
                    k: key_to_char(k)
                    for k in {
                        (1, 2),
                        (1, 1),
                        (0, 1),
                    }
                },
                id="top_left",
            ),
            param(
                init_grid(size=(3, 3)),
                (-1, 3),
                {k: key_to_char(k) for k in {(0, 2)}},
                id="top_left_outside",
            ),
            param(
                init_grid(size=(3, 3)),
                (-2, -2),
                {},
                id="none",
            ),
        ],
    )
    def test_adj(
        self, g: Grid, to: Tuple[int, int], want: Dict[Tuple[int, int], str]
    ) -> None:
        assert dict(g.adj(to)) == want


@mark.parametrize(
    ["dct", "g", "want"],
    [
        param(
            ["dog", "dig", "dug"],
            init_grid(
                size=(4, 4),
                chars=unpack_sequences(
                    [
                        ["d", "o", "g", "i"],
                        ["i", "u", "g", "i"],
                        ["i", "i", "i", "i"],
                        ["d", "g", "i", "i"],
                    ]
                ),
            ),
            {
                (("d", "o", "g"), ((0, 0), (1, 0), (2, 0))),
                (("d", "o", "g"), ((0, 0), (1, 0), (2, 1))),
                (("d", "u", "g"), ((0, 0), (1, 1), (2, 1))),
                (("d", "u", "g"), ((0, 0), (1, 1), (2, 0))),
                (("d", "i", "g"), ((0, 3), (0, 2), (1, 3))),
                (("d", "i", "g"), ((0, 3), (1, 2), (1, 3))),
                (("d", "i", "g"), ((0, 3), (1, 2), (2, 1))),
            },
            id="repeat",
        ),
    ],
)
def test_solve(
    dct: Iterable[str], g: Grid, want: Set[Tuple[Tuple[str], Path, int]]
) -> None:
    assert set(solve(Node.from_keys(dct), g)) == want
