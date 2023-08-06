from copy import deepcopy
from typing import List


def generate_sequence_of_indexes(all_indexes: List[int], diff_indexes: List[int]) -> List[int]:
    if not diff_indexes:
        return all_indexes

    len_diff_indexes = len(diff_indexes)

    if all_indexes:
        len_all_indexes = len(all_indexes)
    else:
        all_indexes = deepcopy(diff_indexes)
        len_all_indexes = len_diff_indexes

    reversed_diff_indexes = deepcopy(diff_indexes)
    reversed_diff_indexes.reverse()

    sequence = list()
    boundary_position = len_all_indexes - 1

    for rev_index in reversed_diff_indexes:
        sequence.append(rev_index)
        boundary_position -= 1

        if boundary_position == 0:
            break

        for index in all_indexes[:boundary_position]:
            if index == rev_index:
                continue
            sequence.append(index)
            sequence.append(rev_index)

    start_position = 0 if len_all_indexes == len_diff_indexes \
        else len_all_indexes - len_diff_indexes - 1

    for index in all_indexes[start_position:]:
        sequence.append(index)

    return sequence
