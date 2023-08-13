from typing import Iterable, Mapping

from pytest import mark, param

from . import spelling_bee as sb
from . import trie


@mark.parametrize(
    ["dct", "optional", "required", "want"],
    [
        param(
            ["do", "dog", "dig"],
            "dogi",
            "g",
            {"dog": 0, "dig": 0},
            id="all_required",
        ),
        param(
            ["do", "dog", "dig"],
            "dog",
            "",
            {"do": 0, "dog": 0},
            id="only_optional",
        ),
        param(
            ["do", "dog", "dig"],
            "dog",
            "g",
            {"dog": 0},
            id="optional_and_required",
        ),
        param(
            ["a", "ab", "abc", "abcd", "abcde", "abcdef"],
            "abcdef",
            "a",
            {"a": 0, "ab": 0, "abc": 0, "abcd": 1, "abcde": 5, "abcdef": 13},
            id="scoring",
        ),
    ],
)
def test_solve(
    dct: Iterable[str],
    optional: Iterable[str],
    required: Iterable[str],
    want: Mapping[str, int],
) -> None:
    assert dict(sb.solve(trie.Node.from_keys(dct), optional, required)) == want
