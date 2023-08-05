import importlib
from enum import Enum
from typing import List, Dict, Any


class AutoName(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: List) -> str:
        return name


class ShadowGlobal:
    """
    magic happens here, any change via `shadow_global` can be recovered
    """
    def __init__(self):
        self.origin = {}
        self.extras = []

    def shadow_global(self, new_global: Dict[str, Any], globals_: Dict = None):
        globals_ = globals_ or globals()
        # pop extra variables
        for extra in self.extras:
            globals_.pop(extra, None)
        self.extras = []
        # recover origin variables
        globals_.update(self.origin)
        self.origin = {}
        # restore origin and extras
        for var_name in new_global:
            if var_name in globals_:
                self.origin[var_name] = globals_[var_name]
            else:
                self.extras.append(var_name)
        globals_.update(new_global)


class ImportMixInGlobal:
    def __init__(self):
        self.sg = ShadowGlobal()
        self.imported = set()

    def import_module_globally(self, path: str | List[str], globals_: Dict = None):
        if isinstance(path, List):
            module_all = self.imports_as_dict(path)
        else:
            module_all = self.import_as_dict(path)
        self.sg.shadow_global(module_all, globals_)

    @staticmethod
    def import_as_dict(path: str) -> Dict[str, Any]:
        mdl = importlib.import_module(path)
        if "__all__" in mdl.__dict__:
            items = mdl.__dict__["__all__"]
        else:
            items = [item for item in mdl.__dict__ if not item.startswith("_")]
        return {
            item: getattr(mdl, item) for item in items
        }

    @staticmethod
    def imports_as_dict(path: List[str]) -> Dict[str, Any]:
        module_all = {}
        for p in path:
            module_all.update(ImportMixInGlobal.import_as_dict(p))
        return module_all
