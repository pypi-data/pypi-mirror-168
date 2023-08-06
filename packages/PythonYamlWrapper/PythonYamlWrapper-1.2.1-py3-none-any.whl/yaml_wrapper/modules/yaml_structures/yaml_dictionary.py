from dataclasses import dataclass
from typing import Union, List, Any
@dataclass
class YamlDictionary:
    key: str
    value: Union[int, str, "YamlDictionary", List["YamlDictionary"], Any]   