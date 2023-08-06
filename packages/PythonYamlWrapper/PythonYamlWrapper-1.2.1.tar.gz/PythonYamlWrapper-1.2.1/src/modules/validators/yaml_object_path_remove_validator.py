from typing import Any, List
from typing import Callable

from ..validators.abstracts.validator import Validator

class YamlObjectPathRemoveValidator(Validator):
    def __init__(self) -> None:
       pass
   
    def validate(self, value: str) -> bool:
        values_splitted: List[str] = value.split(".")
        for item in values_splitted:
            if item == "[]":
                return False
        
        return True