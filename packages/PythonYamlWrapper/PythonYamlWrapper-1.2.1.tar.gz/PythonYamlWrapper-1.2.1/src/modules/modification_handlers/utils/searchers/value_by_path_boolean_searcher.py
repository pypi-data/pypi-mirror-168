from typing import List, Any
from typing import Union

from ....yaml_structures.yaml_dictionary import YamlDictionary
from ....yaml_structures.yaml_list import YamlList

class ValueByPathBooleanSearcher:
    @staticmethod
    def search(filters: List[str], value: Union[str, int], search_in_objects: list) -> bool:
        return ValueByPathBooleanSearcher._search_recursion(filters, value, search_in_objects, True)
    
    @staticmethod
    def _search_recursion(filters: List[str], value: Union[str, int], search_in_objects: list, returned_value: bool) -> bool:
        if len(filters) == 0:
            if len(search_in_objects) > 0 :
                first_search_object_str_int: str = search_in_objects.pop(0)
                if ((isinstance(first_search_object_str_int, str) or isinstance(first_search_object_str_int, int)) and 
                        (first_search_object_str_int == value)):
                    return True
                else:
                    return False
                
            return returned_value
        else:
            first_filter: str = filters.pop(0)
            first_search_object: Union[YamlDictionary, YamlList ] = search_in_objects.pop(0)
            if first_filter != "[]":
                if isinstance(first_search_object, YamlList):
                    raise Exception
                
                if isinstance(first_search_object, list):
                    sub_returned_value: bool = False
                    for sub_item in first_search_object:
                        sub_returned_value = sub_returned_value or ValueByPathBooleanSearcher._search_recursion([first_filter] + filters.copy(), value, [sub_item], True)
                    
                    return ValueByPathBooleanSearcher._search_recursion([], value, [], returned_value and sub_returned_value)
                
                elif isinstance(first_search_object, YamlDictionary) and first_search_object.key == first_filter:
                    
                    return ValueByPathBooleanSearcher._search_recursion(filters, value, [first_search_object.value], returned_value and True)
                else:
                    
                    return ValueByPathBooleanSearcher._search_recursion(filters, value, [first_search_object], returned_value and False)
                                  
            else:
                if first_filter == "[]":
                    if not isinstance(first_search_object, YamlList):
                        raise Exception
               
                return ValueByPathBooleanSearcher._search_recursion(filters, value, first_search_object.values, returned_value and True) # type: ignore