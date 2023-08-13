from __future__ import annotations

from fractions import Fraction
from typing import Iterable, Iterator, List, Sequence, TextIO, Tuple

import click

from . import trie


def sort(keys: Iterable[str]) -> List[str]:
    return sorted(keys, key=len, reverse=True)


def join(letters: Iterable[str]) -> str:
    return "".join(letters)


def containing(dct: trie.Node[str], key: str) -> Iterator[str]:
    for seq, node in dct.search(key):
        yield from map(lambda suffix: join((*seq, *suffix)), node.keys())


def solve(dct: trie.Node[str], contains: str, count: int = 5) -> Tuple[str, ...]:
    words = sort(containing(dct, contains))
    return tuple(words[:count])


def score(
    words: Iterable[str], max: int = 0, sorted: bool = False
) -> Tuple[Fraction, int]:
    if not sorted:
        words = sort(words)
    elif not isinstance(words, Sequence):
        words = list(words)
    return (
        Fraction(len(words[0]), max)  # Longest found w.r.t. longest possible.
        if max
        else Fraction(1)  # Assume longest found is longest possible.
    ), sum(len(key) for key in words)


@click.command()
@click.option(
    "dct", "--dictionary", "-d", type=click.File("r"), envvar="PYWORD_DICTIONARY"
)
@click.argument("contains")
def cli(dct: TextIO | None, contains: str) -> None:
    if dct is None:
        raise Exception("no dictionary provided")

    click.echo("loading dictionary...", err=True, nl=False)
    tr = trie.Node.from_keys(word.strip() for word in dct)
    click.echo(f" ok ({len(tr)} words, {tr.size()} nodes)", err=True)  # type: ignore

    words = solve(tr, contains)
    if not words:
        return

    letters = sum(len(word) for word in words)

    print(words[0], len(words[0]))
    for word in words[1:]:
        print(word, len(word))
    print(f"({letters})")


if __name__ == "__main__":
    cli()
