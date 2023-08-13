from __future__ import annotations

import sys
from itertools import chain
from queue import PriorityQueue
from typing import (
    Dict,
    FrozenSet,
    Iterable,
    Iterator,
    List,
    Optional,
    Set,
    TextIO,
    Tuple,
)

import click

from . import trie

# TODO: Possible culprit for high memory use by storing duplicates rather than using a
#  handle. Need a FrozenSet that hashes by id().
Edge = FrozenSet[str]


class Word(Tuple[Tuple[Edge, str], ...]):
    def edges(self) -> EdgeSet:
        edges: Dict[Edge, Set[str]] = {}
        for edge, char in self:
            edges.setdefault(edge, set()).add(char)
        return EdgeSet(frozenset(chars) for chars in edges.values())


class EdgeSet(FrozenSet[Edge]):
    def words(self, dct: trie.Node[str]) -> Iterator[Word]:
        todo: List[Tuple[trie.Node[str], Word]] = []
        for char, v in dct.next.items():
            for next in self:
                if char in next:
                    todo.append((v, Word(((next, char),))))
        while todo:
            u, path = todo.pop()
            if u.ok:
                yield path
            for char, v in u.next.items():
                prev = path[-1][0]
                for next in self:
                    # Do not use same edge twice in a row.
                    if next is prev:
                        continue
                    if char in next:
                        todo.append((v, Word((*path, (next, char)))))


def count(it: Iterator) -> int:
    return sum(1 for _ in it)


def find_adj(words: Set[Word]) -> Dict[Word, Set[Word]]:
    return {
        prev: {next for next in words if prev[-1][1] == next[0][1]} for prev in words
    }


def solve(
    dct: trie.Node[str], edges: EdgeSet, max_words: int, max_solutions: int
) -> Iterator[Tuple[Word, ...]]:
    if max_words == 0:
        return

    if max_solutions == 0:
        return

    # Find words that are possible according to the game rules and arrange by adjacent
    # i.e. which next words can follow prev word.
    adj = find_adj(set(edges.words(dct)))

    # Remove 1 char words as these can not advance the solution.
    adj = {
        prev: {next for next in nexts if len(next) > 1}
        for prev, nexts in adj.items()
        if len(prev) > 1
    }

    # Prune BFS to not search paths longer than the best outcome so far.
    best: Tuple[Word, ...] = ()
    todo: PriorityQueue[Tuple[int, Tuple[Word, ...]]] = PriorityQueue()
    for word in adj:
        todo.put_nowait((1, (word,)))

    # Sometimes the word list might contain some words not recognised by the game.
    # Allow emitting additional solutions of same length as a workaround without having
    # to do an exhaustive search.
    num_solutions = 0

    while not todo.empty():
        _depth, words = todo.get_nowait()

        if best and len(words) > len(best):
            continue

        chars = Word(chain.from_iterable(words))

        # TODO: Looking for fewest chars is still hard.
        # if best and len(chars) >= sum(1 for _ in chain.from_iterable(best)):
        #     continue

        if chars.edges() == edges:
            yield words
            best = words
            num_solutions += 1
            if num_solutions >= max_solutions > 0:
                return

        if 0 < max_words <= len(words):
            continue

        prev = words[-1]
        for next in adj[prev]:
            todo.put_nowait((len(words) + 1, (*words, next)))


def solves(
    dct: trie.Node[str], edges: EdgeSet, max_words: int, max_solutions: int
) -> Iterator[Tuple[str, ...]]:
    seen: Set[Tuple[str, ...]] = set()
    for words in solve(dct, edges, max_words, max_solutions):
        path = tuple("".join(char[1] for char in word) for word in words)
        if path not in seen:
            yield path
            seen.add(path)


@click.command()
@click.option(
    "--dictionary", "-d", "dct_file", type=click.File("r"), envvar="PYWORD_DICTIONARY"
)
@click.option("--max-solutions", "-o", type=int, default=1)
@click.argument("max_words", type=int)
@click.argument("edges", type=str, nargs=-1)
def cli(
    dct_file: Optional[TextIO], edges: Iterable[str], max_words: int, max_solutions: int
) -> None:
    if not dct_file:
        raise Exception("no dictionary provided")

    print("loading dictionary...", end="", file=sys.stderr, flush=True)
    dct = trie.Node.from_keys(map(str.strip, dct_file))
    print(f" ok ({len(dct)} words, {dct.size()} nodes)", file=sys.stderr, flush=True)

    for words in solves(
        dct,
        EdgeSet(frozenset(edge) for edge in edges),
        max_words,
        max_solutions,
    ):
        print(words, flush=True)
