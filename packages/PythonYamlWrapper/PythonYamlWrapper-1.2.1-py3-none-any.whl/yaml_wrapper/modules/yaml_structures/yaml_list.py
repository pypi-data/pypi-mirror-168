from dataclasses import dataclass
from typing import Union, List, Any

from ..yaml_structures.yaml_dictionary import YamlDictionary

@dataclass
class YamlList:
    values: Union[List["YamlDictionary"], List[Any]]