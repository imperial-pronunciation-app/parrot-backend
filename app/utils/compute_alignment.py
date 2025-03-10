from collections import deque
from enum import Enum, auto
from typing import Callable, List, Optional, Tuple, TypeVar

import numpy as np


T = TypeVar("T")

class AlignmentOperation(Enum):
    MATCH = auto()
    DELETION = auto()
    INSERTION = auto()

def compute_alignment(
    expected: List[T],
    actual: List[T],
    similarity_func: Callable[[T, T], float],
    deletion_penalty: float,
    insertion_penalty: float,
) -> Tuple[List[Tuple[Optional[T], Optional[T]]], int]:
    """
    Generalized function to align two sequences using dynamic programming.

    :param expected: List of expected items.
    :param actual: List of actual items.
    :param similarity_func: Function to compute similarity between items of type `T`.
    :param deletion_penalty: Penalty for missing an expected item. This can vary between different levels.
    :param insertion_penalty: Penalty for adding an extra item. This can vary between different levels.
    :return: Tuple of aligned sequences and a score (0-100).
    """

    if not expected:
        raise ValueError("Expected list must not be empty.")

    if not actual:
        return [(item, None) for item in expected], 0  # All expected items are missing.

    n, m = len(expected), len(actual)
    score_dp = np.zeros((n + 1, m + 1))
    operation_trace = np.zeros((n + 1, m + 1), dtype=AlignmentOperation)

    for i in range(1, n + 1):
        score_dp[i][0] = score_dp[i - 1][0] + deletion_penalty
        operation_trace[i][0] = AlignmentOperation.DELETION

    for j in range(1, m + 1):
        score_dp[0][j] = score_dp[0][j - 1] + insertion_penalty 
        operation_trace[0][j] = AlignmentOperation.INSERTION 

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match_score = similarity_func(expected[i - 1], actual[j - 1])
            choices = [
                (score_dp[i - 1][j - 1] + match_score, AlignmentOperation.MATCH),  # Match or substitution
                (score_dp[i - 1][j] + deletion_penalty, AlignmentOperation.DELETION),  # Deletion
                (score_dp[i][j - 1] + insertion_penalty, AlignmentOperation.INSERTION)  # Insertion
            ]
            score_dp[i][j], operation_trace[i][j] = max(choices, key=lambda x: x[0])

    # Backtracking to extract alignment
    i, j = n, m
    alignment: deque[Tuple[Optional[T], Optional[T]]] = deque()
    while i > 0 or j > 0:
        match operation_trace[i][j]:
            case AlignmentOperation.INSERTION:
                alignment.appendleft((None, actual[j - 1]))
                j -= 1
            case AlignmentOperation.DELETION:
                alignment.appendleft((expected[i - 1], None))
                i -= 1
            case AlignmentOperation.MATCH:
                alignment.appendleft((expected[i - 1], actual[j - 1]))
                i -= 1
                j -= 1
            case _:
                raise ValueError("Invalid operation_trace operation.")

    final_score = int((score_dp[n][m] / max(1, n)) * 100)  # Normalize to 0-100

    return list(alignment), max(0, min(100, final_score))  # Clamp score between 0-100
