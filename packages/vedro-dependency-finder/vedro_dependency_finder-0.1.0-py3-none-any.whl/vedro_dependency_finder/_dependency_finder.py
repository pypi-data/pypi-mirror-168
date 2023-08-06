import os
from pathlib import Path

from vedro.core import ConfigType, Dispatcher, Plugin, PluginConfig
from vedro.events import ArgParsedEvent, ArgParseEvent, ConfigLoadedEvent

from ._dependency_scheduler import DependencyScheduler


class DependencyFinderPlugin(Plugin):
    def subscribe(self, dispatcher: Dispatcher) -> None:
        dispatcher.listen(ConfigLoadedEvent, self.on_config_loaded) \
            .listen(ArgParseEvent, self.on_arg_parse) \
            .listen(ArgParsedEvent, self.on_arg_parsed)

    def on_config_loaded(self, event: ConfigLoadedEvent) -> None:
        self._global_config: ConfigType = event.config

    def on_arg_parse(self, event: ArgParseEvent) -> None:
        group = event.arg_parser.add_argument_group("DependencyFinder")

        group.add_argument(
            "--dependency-finder", nargs="+", default=set(), type=lambda x: Path(x).absolute(),
            help="Generates a sequence of tests at startup to detect unstable tests"
        )

    def on_arg_parsed(self, event: ArgParsedEvent) -> None:
        scenarios_paths = event.args.dependency_finder

        for path in scenarios_paths:
            assert not os.path.isdir(path), f"scenarios expected, not directory {path!r}"
            assert os.path.isfile(path), f"{path!r} does not exist"

        self._global_config.Registry.ScenarioScheduler.register(
            lambda scenarios: DependencyScheduler(
                scenarios=scenarios,
                scenarios_paths=scenarios_paths,
            ), self
        )


class DependencyFinder(PluginConfig):
    plugin = DependencyFinderPlugin
