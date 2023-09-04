import pkgutil
import importlib
from src.config import PLUGINS_PATH


class PluginManager:
    _inst = None

    def _search_plugins(self) -> list:
        return [
            importlib.import_module(f"plugins.{name}")
            for _, name, _
            in pkgutil.iter_modules([PLUGINS_PATH])
        ]

    def get_events_statuses(self) -> dict[str, bool]:
        return {
            mod.__plugin_name__: mod.happened()
            for mod in self._inst._plugins
        }

    def get_events_names(self) -> list[str]:
        return [
            mod.__plugin_name__
            for mod in self._inst._plugins
        ]

    def __new__(cls, *args, **kwargs):
        if cls._inst is None:
            cls._inst = object.__new__(cls)
            cls._inst._plugins = cls._inst._search_plugins()
        return cls._inst

# TODO Need to check that event already happened
