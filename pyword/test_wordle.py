from collections import Counter
from typing import List

from pytest import mark, param

from . import wordle


@mark.parametrize(
    ["ans", "guess", "want"],
    [
        param(
            "latte",
            "wheel",
            [
                wordle.Answer.Result.NO,
                wordle.Answer.Result.NO,
                wordle.Answer.Result.POS,
                wordle.Answer.Result.NO,
                wordle.Answer.Result.POS,
            ],
            id="repeat_pos",
        ),
        param(
            "hello",
            "hello",
            [
                wordle.Answer.Result.YES,
                wordle.Answer.Result.YES,
                wordle.Answer.Result.YES,
                wordle.Answer.Result.YES,
                wordle.Answer.Result.YES,
            ],
            id="correct",
        ),
        param(
            "youth",
            "earls",
            [
                wordle.Answer.Result.NO,
                wordle.Answer.Result.NO,
                wordle.Answer.Result.NO,
                wordle.Answer.Result.NO,
                wordle.Answer.Result.NO,
            ],
            id="none",
        ),
        param(
            "solar",
            "rails",
            [
                wordle.Answer.Result.POS,
                wordle.Answer.Result.POS,
                wordle.Answer.Result.NO,
                wordle.Answer.Result.POS,
                wordle.Answer.Result.POS,
            ],
            id="pos",
        ),
    ],
)
def test_guess_answer(ans: str, guess: str, want: List[wordle.Answer.Result]) -> None:
    assert wordle.Answer(ans).guess(guess) == want


@mark.parametrize(
    ["f", "w", "ok"],
    [
        param(
            wordle.Facts(
                pos=Counter(
                    {
                        "s": 3,
                    }
                )
            ),
            "soups",
            True,
            id="pos_gt",
        ),
        param(
            wordle.Facts(
                pos=Counter(
                    {
                        "s": 2,
                    }
                )
            ),
            "soups",
            True,
            id="pos_eq",
        ),
        param(
            wordle.Facts(
                pos=Counter(
                    {
                        "s": 1,
                    }
                )
            ),
            "soups",
            False,
            id="pos_lt",
        ),
        param(
            wordle.Facts(
                no={
                    4: {"s"},
                },
            ),
            "soups",
            False,
            id="no",
        ),
        param(
            wordle.Facts(),
            "soups",
            True,
            id="ok",
        ),
    ],
)
def test_facts_possible(f: wordle.Facts, w: str, ok: bool) -> None:
    assert f.possible(w) is ok
