from pytest import mark, param

from .trie import Node


class TestTrie:
    @mark.parametrize(
        ["key"],
        [
            param("trie", id="unique"),
            param("lolol", id="repeat"),
        ],
    )
    def test_first(self, key: str) -> None:
        tr: Node[str] = Node()
        assert len(tr) == 0
        assert key not in tr

        tr.add(key)
        assert len(tr) == 1
        assert key in tr
        assert tr.size() == len(key)

        tr.remove(key)
        assert len(tr) == 0
        assert key not in tr
        assert tr.size() == len(key)

    def test_branch(self) -> None:
        keys = (tuple("branch"), tuple("brunch"))

        tr: Node[str] = Node()
        assert len(tr) == 0

        for i, key in enumerate(keys, start=1):
            assert key not in tr
            tr.add(key)
            assert len(tr) == i

        assert tr.size() == 10
        assert set(tr) == set(keys)

        for i, key in enumerate(keys, start=1):
            assert key in tr
            tr.remove(key)
            assert len(tr) == len(keys) - i

        assert tr.size() == 10
