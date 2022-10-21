from typing import Callable, Dict, Tuple

from pytest import mark, param

from .boggle import Grid


def key_to_char(k: Tuple[int, int]) -> str:
    return f"{k[0]}.{k[1]}"


def init_grid(
    size: Tuple[int, int] = (4, 4),
    chars: Callable[[Tuple[int, int]], str] = key_to_char,
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
