from typing import Iterable, Iterator, List, Tuple

from .trie import Trie


def solve(
    dct: Iterable[str], optional: Iterable[str], required: Iterable[str] = ""
) -> Iterator[Tuple[str, int]]:
    if not isinstance(dct, Trie):
        dct = Trie.from_keys(dct)
    if not isinstance(optional, set):
        optional = set(optional)
    if not isinstance(required, set):
        required = set(required)
    optional.update(required)

    def score(w: str) -> int:
        # Must be 4 chars or more.
        if len(w) < 4:
            return 0
        # Must only contain optional chars.
        c = set(w)
        assert isinstance(optional, set)
        if c - optional:
            return 0
        # Must contain all required chars.
        assert isinstance(required, set)
        if required - c:
            return 0
        # One point for every char over 3 chars.
        p = len(w) - 3
        # Bonus points if all optional chars used.
        if not optional - c:
            p += 7
        return p

    # Seed search with words starting with any char from list.
    s: List[Tuple[str, Trie]] = [  # type: ignore
        (c, u) for c in optional if (u := dct.next.get(c)) is not None
    ]
    while s:
        w, u = s.pop()
        # Solution if is a word and all required chars used.
        if u.ok and not required - set(w):
            yield w, score(w)
        # Extend search with any next char from list.
        for c in optional:
            if (v := u.next.get(c)) is not None:
                s.append((w + c, v))
