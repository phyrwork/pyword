from . import linear, trie


def test_solve() -> None:
    dct = trie.Node.from_keys(
        {
            "okay",
            "this",
            "should",
            "be",
            "easy",
        }
    )

    grid = linear.Grid(
        "bpxtgbezvhdn",
        "peasyshouldg",
        "rspthisyzdzz",
        "oymgcvxecshd",
        "bedztokdxqtu",
        "zokaytqobjzd",
        "nqmlijsdqcsr",
        "ueuiyvtyocsj",
    )

    want = {
        ((5, 1), (5, 2), (5, 3), (5, 4)),  # "okay"
        ((4, 0), (4, 1)),  # "be"
        ((2, 3), (2, 4), (2, 5), (2, 6)),  # "this"
        ((1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10)),  # "should"
        ((1, 1), (1, 2), (1, 3), (1, 4)),  # "easy"
        ((0, 5), (0, 6)),  # "be"
        ((0, 0), (1, 1)),  # "be"
    }
    got = set(linear.solve(dct, grid))

    assert want == got
