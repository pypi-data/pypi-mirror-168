# Vedro Dependency Finder

Plugin helps to find dependencies of unstable tests by shuffling selected tests

## Installation

```shell
$ pip3 install vedro-dependency-finder
```

## Usage

```python
import vedro
import vedro_dependency_finder as df


class Config(vedro.Config):
    class Plugins(vedro.Config.Plugins):
        class DependencyFinder(df.DependencyFinder):
            enabled = True

```
Run several scenarios:
```shell
$ vedro run --dependency-finder scenarios/scenario.py scenarios/another_scenario.py
```

Run all scenarios:
```shell
$ vedro run -vvv --dependency-finder `find scenarios -name "*.py"`
```
