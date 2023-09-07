import pkgutil
import importlib
from threading import Lock
from src.config import PLUGINS_PATH


class PluginManager:
    _inst = None
    _mx = Lock()

    def _search_plugins(self) -> list:
        modules = [
            importlib.import_module(f"plugins.{name}")
            for _, name, _
            in pkgutil.iter_modules([PLUGINS_PATH])
        ]
        return [
            [mod, mod.happened()]
            for mod in modules
        ]

    def get_events_statuses(self) -> dict[str, bool]:
        return {
            mod.__plugin_name__: curr_status
            for mod, curr_status in self._plugins
        }

    def get_happened_events(self) -> list[str]:
        res = []
        for i in range(len(self._plugins)):
            mod, curr_status = self._plugins[i]
            if curr_status:
                continue
            if mod.happened():
                self._plugins[i][1] = True
                res.append(mod.__plugin_name__)
        return res

    def get_events_names(self) -> list[str]:
        return [
            mod.__plugin_name__
            for mod, curr_status in self._plugins
        ]

    def __new__(cls, *args, **kwargs):
        if cls._inst is None:
            cls._mx.acquire()
            if cls._inst is None:
                cls._inst = object.__new__(cls)
                cls._inst._plugins = cls._inst._search_plugins()
            cls._mx.release()
        return cls._inst
