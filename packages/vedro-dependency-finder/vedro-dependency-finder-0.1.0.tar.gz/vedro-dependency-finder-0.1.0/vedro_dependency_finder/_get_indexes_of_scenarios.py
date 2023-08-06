from pathlib import Path
from typing import List, Set, Tuple

from vedro.core import VirtualScenario


def get_indexes_of_scenarios(scenarios: List[VirtualScenario],
                             scenarios_paths: Set[Path]) -> Tuple[List[int], List[int]]:
    assert scenarios, "Scenarios not found!"
    assert scenarios_paths, "Paths of scenarios not found!"

    all_indexes = list(range(len(scenarios)))
    diff_indexes = list()

    for index, scenario in enumerate(scenarios):
        if scenario.path in scenarios_paths:
            diff_indexes.append(index)

    assert diff_indexes, "The selected scenarios are not contained in the selected folder!"

    # перемещаем diff_index'ы в конец all_indexes,
    # для правильной генерации последовательности
    for diff_index in diff_indexes:
        all_indexes += [all_indexes.pop(all_indexes.index(diff_index))]

    return all_indexes, diff_indexes
