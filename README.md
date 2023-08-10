# pyword

Word search game solvers written in Python.

[![pyword](https://circleci.com/gh/phyrwork/pyword/tree/master.svg?style=svg)](https://app.circleci.com/pipelines/github/phyrwork/pyword?branch=master)

This repository demonstrates the solving of some common word search games using a
[character trie](https://en.wikipedia.org/wiki/Trie) representation of the valid words
dictionary to prune the search in a very efficient way.

Variations according to specific game rules aside, the general approach is to keep the
trie node associated with the end of each path being searched and use it to prune
traversals to adjacent letters. If an adjacent letter is not an outgoing edge of the
node then the prefix formed by following the letter will never need to a valid word.

The `pyword` package is made up of the `trie` module, where the dictionary `Trie` class
is defined, and modules for each of the word search games a solver is demonstrated for.


## Solvers

The following solvers are demonstrated:

| Game             | Command      | Description                                                                                      |
|------------------|--------------|--------------------------------------------------------------------------------------------------|
| Boggle           | boggle       | Arbitrary **N**x**M** size Boggle solver with scoring based on standard (4x4) rules.             |
| NYT Letter Boxed | letter-boxed | [New York Times Letter Boxed](https://www.nytimes.com/puzzles/letter-boxed) solver.              |
| NYT Spelling Bee | spelling-bee | [New York Times Spelling Bee](https://www.nytimes.com/puzzles/spelling-bee) solver with scoring. |
| Wordiply         | wordiply     | The Guardian [Wordiply](https://www.wordiply.com) solver.                                        |


## Usage

The suggested way to use the solvers is to create and activate a virtual environment
using [Poetry](https://python-poetry.org/docs/) e.g.

```shell
$ poetry install
Installing dependencies from lock file
...
$ poetry run boggle --help
(pyword-py3.10) pyword$ boggle --help
Usage: boggle [OPTIONS] [ROWS]...

Options:
  -d, --dictionary FILENAME
  --help                     Show this message and exit.
```

A path to a dictionary file of line separated words must be provided either as the `--dictionary`
or `-d` option or as the `PYWORD_DICTIONARY` environment variable.

Unix-like systems often have a word list at `/usr/share/dict/words`.


### Boggle

Provide each row of letters as a positional argument. Grid size is auto-detected.

For example, give the grid

```text
h  e  l  l
l  i  k  d
o  qu e  e
l  a  u  n
```

as

```shell
$ boggle hell likd oquee laun
loading dictionary... ok (234371 words, 757961 nodes)
unequal ((2, 3), (3, 3), (2, 2), (1, 2), (1, 3), (0, 3)) 4
needle ((3, 3), (3, 2), (2, 2), (3, 1), (2, 0), (1, 0)) 3
needle ((3, 3), (2, 2), (3, 2), (3, 1), (2, 0), (1, 0)) 3
kildee ((2, 1), (1, 1), (2, 0), (3, 1), (2, 2), (3, 2)) 3
...
(106 words, 172 paths, 95 points)
```


### NYT Letter Boxed

The day's word count target is given as the first positional argument followed by
strings representing the chars of each of the box's edges.

```shell
$ letter-boxed 5 yse rio vfq dut
loading dictionary... ok (194433 words, 447873 nodes)
('requoted', 'diversify')
```

Though _Letter Boxed_ is 4 edges of 3 chars each, the solver does not have any
restriction on edge or chars-per-edge count.

```shell
$ letter-boxed 5 ys erio vfq             
loading dictionary... ok (194433 words, 447873 nodes)
('qi', 'iso', 'of', 'five', 'eyry')
```

By default only one optimal solution is emitted. If you need more solutions e.g.
because the game does not recognise some entries from your word list then you can
emit additional solutions.

```shell
$ letter-boxed 5 yse rio vfq dut -o 3
loading dictionary... ok (194433 words, 447873 nodes)
('requoted', 'diversify')
('quoted', 'diversify')
('videofits', 'surquedry')
```


### NYT Spelling Bee

The day's optional characters are given as a string as the first positional argument.
Any mandatory characters are given as the second argument.

```shell
$ spelling-bee dncioe v
loading dictionary... ok (235886 words, 792776 nodes)
inconvinced 15
convinced 13
codivine 12
...
(86 words, 257 points)
```


### Wordiply

The day's subword is given as the argument.

The letter score is printed after the best 5 discovered words. No length score can be given as the contents of the
common word dictionary is not known. For example `mitrailleuses` as discovered below was not in the common word list and
so the length score was >100%.

```shell
$  wordiply rail                                           
loading dictionary... ok (194433 words, 447873 nodes)
mitrailleuses 13
semitrailers 12
mitrailleuse 12
mitrailleurs 12
engrailments 12
61
```
