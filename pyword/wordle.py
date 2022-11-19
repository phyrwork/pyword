from collections import Counter
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Set


class SizeError(Exception):
    ...


class Answer(str):
    class Result(Enum):
        NO = auto()
        POS = auto()
        YES = auto()

    def guess(self, guess: str) -> List[Result]:
        if len(guess) != len(self):
            raise SizeError(f"query size {len(guess)} != answer size {len(self)}")

        n: Counter[str] = Counter(self)

        def pop(c: str) -> bool:
            if ok := n[c] > 0:
                n[c] -= 1
            return ok

        def at(i: int, c: str) -> Answer.Result:
            ok = pop(c)
            return (
                Answer.Result.YES
                if c == self[i]
                else Answer.Result.POS
                if ok
                else Answer.Result.NO
            )

        return [at(i, c) for i, c in enumerate(guess)]


@dataclass
class Facts:
    pos: Counter[str] = field(default_factory=Counter)
    no: Dict[int, Set[str]] = field(default_factory=dict)

    def possible(self, w: str) -> bool:
        for i, c in enumerate(w):
            if c in self.no.get(i, set()):
                return False
        n = Counter(w)
        for c, i in self.pos.items():
            if n[c] > i:
                return False
        return True
