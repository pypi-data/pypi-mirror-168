"""A collection of filters to use with feyn Models."""

from typing import List, Union

import feyn


class Complexity:
    """Use this class to get a filter for selecting models with a specific complexity."""

    def __init__(self, complexity: int):
        self.complexity = int(complexity)

    def __call__(self, model: feyn.Model) -> bool:
        return model.edge_count == self.complexity


class ContainsInputs:
    """Use this class to get a filter for including only models that contain specific named inputs."""

    def __init__(self, input_name: Union[str, List[str]]):
        if isinstance(input_name, str):
            input_name = [input_name]

        self.names = input_name

    def __call__(self, model: feyn.Model) -> bool:
        return all(name in model.inputs for name in self.names)


class ExcludeFunctions:
    """Use this class to get a filter for excluding models that contain any of the named functions."""

    def __init__(self, functions: Union[str, List[str]]):
        if isinstance(functions, str):
            functions = [functions]

        self.functions = functions

    def __call__(self, model: feyn.Model) -> bool:
        for e in model:
            if e.fname in self.functions:
                return False

        return True



class ContainsFunctions:
    """Use this class to get a filter for including only models that exclusively consist of the named functions."""

    def __init__(self, functions: Union[str, List[str]]):
        if isinstance(functions, str):
            functions = [functions]

        self.functions = functions

    def __call__(self, model: feyn.Model) -> bool:
        used_functions = [e.fname.split(":")[0] for e in model if e.name == ""]
        return used_functions == self.functions
