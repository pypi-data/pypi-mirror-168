from pathlib import Path
from typing import List, Set

from vedro.core import MonotonicScenarioScheduler, ScenarioScheduler, VirtualScenario

from ._generate_sequence_of_indexes import generate_sequence_of_indexes
from ._get_indexes_of_scenarios import get_indexes_of_scenarios


class DependencyScheduler(MonotonicScenarioScheduler):
    def __init__(self, scenarios: List[VirtualScenario], scenarios_paths: Set[Path]) -> None:
        super().__init__(scenarios)
        self._scenarios_paths = scenarios_paths

    def __aiter__(self) -> "ScenarioScheduler":
        scenarios = [scn for scn, _ in self._scheduled.values()]

        if self._scenarios_paths:
            all_indexes, diff_indexes = get_indexes_of_scenarios(
                scenarios, self._scenarios_paths
            )
            sequence_of_indexes = generate_sequence_of_indexes(all_indexes, diff_indexes)

            self._scenarios = list()
            for index in sequence_of_indexes:
                self._scenarios.append(scenarios[index])
        else:
            self._scenarios = scenarios

        return super().__aiter__()

    async def __anext__(self) -> VirtualScenario:
        while len(self._scenarios) > 0:
            return self._scenarios.pop()
        raise StopAsyncIteration()
