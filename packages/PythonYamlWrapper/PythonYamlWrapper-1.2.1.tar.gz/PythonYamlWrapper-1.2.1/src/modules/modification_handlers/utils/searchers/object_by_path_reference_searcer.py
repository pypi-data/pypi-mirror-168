from typing import List, Any
from typing import Union
from typing import cast
from ....yaml_structures.exceptions.list_not_respect_integrity import ListNotRespectIntegriry
from ....yaml_structures.yaml_dictionary import YamlDictionary
from ....yaml_structures.yaml_list import YamlList

class ObjectByPathReference:
    @staticmethod
    def search(filters: List[str], search_in_objects: List[Any]) -> Union[YamlDictionary, YamlList, None]:
        return ObjectByPathReference._search_recursion(filters, search_in_objects, cast(Union[YamlDictionary, YamlList], {}))
    
    @staticmethod
    def _search_recursion(filters: List[str], search_in_objects: list, returned_value: Union[YamlDictionary, YamlList, None]) -> Union[YamlDictionary, YamlList, None]:
        if len(filters) == 0:
            return returned_value
        else:
            for item in search_in_objects:
                first_filter: str = filters[0]
                
                if (isinstance(item, YamlDictionary) and 
                    cast(YamlDictionary, item).key == first_filter):
                    
                    if(len(filters[1:]) > 0) and  ((not isinstance(item.value, int)) or (not isinstance(item.value, int))):
                        return ObjectByPathReference._search_recursion(filters[1:], cast(list, item.value), None)
                    else:
                        search_in_objects.pop(search_in_objects.index(item))
                        return ObjectByPathReference._search_recursion([], [], item)
                    
            return  None