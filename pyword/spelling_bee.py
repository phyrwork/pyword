import sys
from typing import Iterable, Iterator, List, Optional, TextIO, Tuple

import click

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


def iter_strip(it: Iterable[str]) -> Iterator[str]:
    for s in it:
        yield s.strip()


@click.command()
@click.option("--dictionary", "-d", type=click.File("r"), envvar="PYWORD_DICTIONARY")
@click.argument("optional", type=str)
@click.argument("required", type=str, default="")
def cli(dictionary: Optional[TextIO], optional: str, required: str) -> None:
    if dictionary is None:
        raise Exception("no dictionary provided")

    print("loading dictionary...", end="", file=sys.stderr, flush=True)
    dct = Trie.from_keys(iter_strip(dictionary))
    print(f" ok ({len(dct)} words, {dct.size()} nodes)", file=sys.stderr, flush=True)

    result = sorted(
        solve(
            dct,
            optional,
            required,
        ),
        key=lambda item: item[1],
        reverse=True,
    )

    for word, score in result:
        print(word, score)

    print(f"({len(result)} words, {sum(score for _, score in result)} points)")


if __name__ == "__main__":
    cli()
