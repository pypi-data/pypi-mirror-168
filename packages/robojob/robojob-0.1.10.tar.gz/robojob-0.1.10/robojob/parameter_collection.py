import re
from typing import Any, Dict


class ParameterCollection:
    def __init__(self, parameters : Dict = {}):
        self.parameters = dict(parameters)

    def normalize_name(self, name):
        return "".join(re.findall(r"[^\W_]", str(name).lower()))

    def __setitem__(self, name: str, value: Any) -> None:
        self.parameters[self.normalize_name(name)] = value

    def __getitem__(self, name: str) -> Any:
        normalized_name = self.normalize_name(name)
        if normalized_name in self.parameters:
            return self.parameters[normalized_name]
        else:
            raise KeyError(f"The parameter '{name}' is not defined.")

    def __contains__(self, name):
        return self.normalize_name(name) in self.parameters

    def update(self, input_dict : Dict) -> None:
        for name, value in input_dict.items():
            self[name] = value
            
    def get(self, name: str, default_value: Any=None) -> Any:
        normalized_name = self.normalize_name(name)
        if normalized_name in self.parameters:
            return self.parameters[normalized_name]
        else:
            return default_value

    def copy(self):
        return ParameterCollection(self.parameters)
