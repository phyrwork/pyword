from . import letter_boxed as lb
from . import trie


class TestPath:
    def test_used(self) -> None:
        a = frozenset(("h", "t", "n"))
        b = frozenset(("i", "o", "e"))

        path = lb.Word(
            (
                (a, "h"),
                (b, "i"),
                (a, "t"),
                (b, "o"),
                (a, "n"),
                (b, "o"),
                (a, "n"),
                (b, "e"),
            )
        )

        want = {a, b}
        got = path.edges()

        assert got == want


class TestEdgeSet:
    def test_words(self) -> None:
        a = frozenset(("h", "t", "i"))
        b = frozenset(("i", "a", "t"))

        dct = trie.Node.from_keys(
            (
                "it",
                "hit",
                "at",
                "hat",
                "tat",
                "twit",
            )
        )

        edges = lb.EdgeSet((a, b))

        want = {
            ((a, "i"), (b, "t")),
            ((b, "i"), (a, "t")),
            ((a, "h"), (b, "i"), (a, "t")),
            ((b, "a"), (a, "t")),
            ((a, "h"), (b, "a"), (a, "t")),
            ((a, "t"), (b, "a"), (a, "t")),
        }
        got = set(edges.words(dct))

        assert got == want


def test_solves() -> None:
    dct = trie.Node.from_keys(
        ("hit", "ton", "none", "hi", "it", "on", "to", "non", "one")
    )
    edges = lb.EdgeSet((frozenset(("h", "t", "n")), frozenset(("i", "o", "e"))))

    got = set(lb.solves(dct, edges, 5, -1))
    want = {("hit", "to", "one"), ("hit", "ton", "none")}

    assert got == want
