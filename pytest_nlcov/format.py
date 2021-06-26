from typing import Iterator
from typing import List
from typing import Tuple


def list_to_ranges(lines: List[int]) -> List[Tuple[int, int]]:
    """Produce a list of ranges for `format_lines`.

    >>> list_to_ranges([1,2,3,4])
    [(1, 4)]
    >>> list_to_ranges([1,4])
    [(1, 1), (4, 4)]
    >>> list_to_ranges([1,2,4,5,7])
    [(1, 2), (4, 5), (7, 7)]
    >>> list_to_ranges([-2, -1, 0, 1])
    [(-2, 1)]
    >>> list_to_ranges([])
    []


    """
    lines = sorted(lines)

    pairs = []
    start = None
    prev_line = None
    for line in lines:
        if start is None:
            start = prev_line = line
            continue

        if line == prev_line + 1:
            prev_line = line
            continue

        pairs.append((start, prev_line))
        start = prev_line = line

    if start and prev_line:
        pairs.append((start, prev_line))

    return pairs


def format_ranges(pairs: List[Tuple[int, int]]) -> Iterator[str]:
    """
    >>> list(format_ranges([(1,2), (3,3), (4,20)]))
    ['1-2', '3', '4-20']
    """
    for (start, end) in pairs:
        if start == end:
            yield f"{start}"
        else:
            yield f"{start}-{end}"


def format_lines(lines: List[int]):
    return ", ".join(format_ranges(list_to_ranges(lines)))
